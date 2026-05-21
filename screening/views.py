import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Resume, Prediction, HRSession
from .ai import extract_text, full_analysis, JOB_CATEGORIES


def home(request):
    """Landing page — choose portal."""
    return render(request, 'screening/home.html')


def candidate(request):
    """Candidate portal — upload one resume and get analysis."""
    result = None
    error = ""

    if request.method == 'POST':
        if 'resume' not in request.FILES:
            error = "No file selected."
        else:
            file = request.FILES['resume']
            allowed = ('.pdf', '.txt', '.doc', '.docx')
            if not any(file.name.lower().endswith(ext) for ext in allowed):
                error = "Only PDF, TXT, DOC, or DOCX files are allowed."
            else:
                resume = Resume.objects.create(file=file, portal='user')
                text = extract_text(resume.file.path)

                if not text.strip():
                    error = "Could not read text from this file."
                elif not full_analysis(text)['is_resume']:
                    error = "This doesn't look like a resume. Please upload a resume document."
                else:
                    analysis = full_analysis(text)
                    Prediction.objects.create(
                        resume=resume,
                        category=analysis['category'],
                        score=analysis['match_pct'],
                        skills_found=', '.join(analysis['skills']),
                        skills_missing=', '.join(analysis['missing']),
                    )
                    # Build category breakdown (top 5)
                    breakdown = sorted(
                        analysis['all_scores'].items(), key=lambda x: x[1], reverse=True
                    )[:5]
                    breakdown = [
                        {
                            'name': cat,
                            'pct': round((score / len(JOB_CATEGORIES.get(cat, [1]))) * 100)
                        }
                        for cat, score in breakdown if score > 0
                    ]
                    result = {
                        'filename': file.name,
                        'category': analysis['category'],
                        'match_pct': analysis['match_pct'],
                        'skills': analysis['skills'],
                        'missing': analysis['missing'],
                        'breakdown': breakdown,
                    }

    return render(request, 'screening/candidate.html', {
        'result': result,
        'error': error,
        'categories': list(JOB_CATEGORIES.keys()),
    })


def hr_dashboard(request):
    """HR portal — render the dashboard page."""
    sessions = HRSession.objects.order_by('-created_at')[:5]
    return render(request, 'screening/hr.html', {
        'categories': list(JOB_CATEGORIES.keys()),
        'recent_sessions': sessions,
    })


@csrf_exempt
def hr_analyze(request):
    """AJAX endpoint — accepts multiple resumes + settings, returns JSON results."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    files = request.FILES.getlist('resumes')
    keywords_raw = request.POST.get('keywords', '')
    category_filter = request.POST.get('category', '').strip()
    min_score = int(request.POST.get('min_score', 40))

    keywords = [k.strip().lower() for k in keywords_raw.split(',') if k.strip()]

    if not files:
        return JsonResponse({'error': 'No files uploaded.'}, status=400)

    session = HRSession.objects.create(
        keywords=keywords_raw,
        category_filter=category_filter,
        min_score=min_score,
    )

    results = []
    for file in files:
        allowed = ('.pdf', '.txt', '.doc', '.docx')
        if not any(file.name.lower().endswith(ext) for ext in allowed):
            continue
        resume = Resume.objects.create(file=file, portal='hr')
        text = extract_text(resume.file.path)
        if not text.strip():
            continue

        analysis = full_analysis(text, hr_keywords=keywords, category_filter=category_filter)

        Prediction.objects.create(
            resume=resume,
            category=analysis['category'],
            score=analysis['final_score'],
            skills_found=', '.join(analysis['skills']),
            skills_missing=', '.join(analysis['missing']),
        )

        results.append({
            'name': file.name,
            'category': analysis['category'],
            'match_pct': analysis['match_pct'],
            'final_score': analysis['final_score'],
            'kw_matched': analysis.get('kw_matched', []),
            'kw_missing': analysis.get('kw_missing', []),
            'kw_score': analysis.get('kw_score', 100),
            'skills': analysis['skills'][:6],
            'missing': analysis['missing'][:5],
            'is_resume': analysis['is_resume'],
        })

    results.sort(key=lambda x: x['final_score'], reverse=True)
    return JsonResponse({'results': results, 'session_id': session.id})


def share(request):
    """Share landing page."""
    portal = request.GET.get('portal', 'candidate')
    return render(request, 'screening/share.html', {'portal': portal})
