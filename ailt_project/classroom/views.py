import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from dotenv import load_dotenv
from .models import Student, Lesson, SessionReport, ActiveSession
from groq import Groq
from django.utils import timezone
from datetime import timedelta

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classroom_ui(request):
    did_key = os.getenv("D_ID_API_KEY")
    
    current_session = ActiveSession.objects.filter(is_active=True).first()
    
    if current_session:
        students = Student.objects.filter(
            year=current_session.year, 
            class_number=current_session.class_number
        ).order_by('name') 
        
        lesson = current_session.active_lesson
    else:
        students = None
        lesson = None

    return render(request, 'classroom/index.html', {    # reponse to GET Request
        'did_key': did_key,
        'students': students,
        'lesson': lesson,
        'current_session': current_session,
    })

@csrf_exempt
def chat_with_ailt(request):    # first-party Web API
    if request.method == 'POST':
        data = json.loads(request.body) # unpacks JSON POST Request from index.html line 244
        user_message = data.get('message')
        student_id = data.get('student_id')
        lesson_id = data.get('lesson_id')
        raw_history = data.get('history', [])

        formatted_history = "\n".join([f"{msg['role']}: {msg['text']}" for msg in raw_history[:-1]])

        try:
            student = Student.objects.get(id=student_id)
            lesson = Lesson.objects.get(id=lesson_id)
        except (Student.DoesNotExist, Lesson.DoesNotExist):
            return JsonResponse({'error': 'Student or Lesson not found'}, status=404)

        system_prompt = f"""
        You are AILT, an Assistant Language Teacher in a Japanese Junior High School.
        The student is: {student.name}. Hobbies: {student.hobbies}.
        The JTE's target grammar is: {lesson.target_grammar}.
        
        Previous Conversation:
        {formatted_history}

        The student just said: "{user_message}"

        Directives:
        1. Start the conversation with a greeting assuming you already know the student.
        2. Acknowledge the student's answer and move the topic forward.
        3. Keep responses short (1-2 sentences) and sound like a natural, friendly human teacher.
        4. Gently recast grammatical errors.
        5. Use the target grammar naturally, but never talk about grammar.
        6. NEVER use Japanese, ALWAYS speak in English.
        7. You MUST output your response as a valid JSON object with EXACTLY ONE key:
           - "reply_to_student": Your conversational response.
        """

        try:
            chat_completion = client.chat.completions.create(       # POST Request to Groq
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ],
                model="llama-3.1-8b-instant",   # also try "llama-3.3-70b-versatile"
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            response_text = chat_completion.choices[0].message.content  # Reply from Groq
            ai_data = json.loads(response_text)
            
            reply = ai_data.get('reply_to_student', "Could you repeat that?")
            
            transcript_entry = f"{student.name}: {user_message}\nAILT: {reply}"
            
            latest_report = SessionReport.objects.filter(
                student=student,
                lesson=lesson
            ).order_by('-date').first()
            
            if latest_report and (timezone.now() - latest_report.date) < timedelta(minutes=50):
                if latest_report.mistakes_logged:
                    latest_report.mistakes_logged += f"\n{transcript_entry}"
                else:
                    latest_report.mistakes_logged = transcript_entry
                        
                latest_report.save()
            else:
                SessionReport.objects.create(
                    student=student,
                    lesson=lesson,
                    mistakes_logged=transcript_entry 
                )
            
        except Exception as e:
            print(f"Error: {e}")
            reply = "I had a little trouble understanding that. Let's try again."

        return JsonResponse({'reply': reply})   # to index.html line 255

def teacher_dashboard(request):
    reports = SessionReport.objects.all().order_by('-date')
    return render(request, 'classroom/dashboard.html', {'reports': reports})

def presentation_ui(request):
    """Loads the Teacher's Big Screen Presentation Mode."""
    did_key = os.getenv("D_ID_API_KEY")
    return render(request, 'classroom/presentation.html', {'did_key': did_key})

@csrf_exempt
def presentation_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message', '')
        history = data.get('history', [])

        messages_for_groq = []
        
        system_prompt = """
        You are an Assistant Language Teacher (ALT) from the UK co-teaching a Japanese Junior High School English class. 
        The Japanese Teacher of English (JTE) has just asked you a question.
        Respond with a short, highly engaging 3-4 sentence monologue about a personal experience. 
        Then, end by asking the class a simple question related to your story.
        Keep the English simple (A1/A2 level). 
        You MUST output your response in valid JSON format with a single key: "reply".
        """
        
        messages_for_groq.append({"role": "system", "content": system_prompt})

        for chat in history[-4:]:
            role = "user" if chat["role"] == "Teacher" else "assistant"
            messages_for_groq.append({"role": role, "content": chat["text"]})
            
        messages_for_groq.append({"role": "user", "content": message})

        try:
            chat_completion = client.chat.completions.create(
                messages=messages_for_groq,
                model="llama-3.3-70b-versatile",    # also try"llama-3.1-8b-instant"
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            ai_response = chat_completion.choices[0].message.content
            parsed_response = json.loads(ai_response)
            
            return JsonResponse({
                "reply": parsed_response.get("reply", "Hello class!")
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Invalid request"}, status=400)