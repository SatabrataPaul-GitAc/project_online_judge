import os
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Problems,TestCases, Solutions
from uuid import uuid4
from pathlib import Path


BASE_URL = "http://localhost:8000"

# Create your views here.
@require_GET
def index(request):
    return HttpResponseRedirect("{}/oj/problems/1".format(BASE_URL))


@require_GET
def home(request, page):
    problem_list = Problems.objects.all()
    paginator = Paginator(problem_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        'problems': page_obj,
        'page': page,
        'next_page': page_obj.has_next(),
        'base_url': BASE_URL
    }
    return render(request, 'index.html', context)


@require_GET
def view_problem(request, code):
    problem = Problems.objects.get(code=code)
    problem_statement = problem.statement
    problem_code = problem.code
    context = {
        'problem': problem_statement,
        'problemcode': problem_code
    }
    return render(request, 'problem.html', context)


@csrf_exempt
@require_POST
def evaluate_code(request, code):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    problem_code = body.get('problem_code', '')
    code = body.get('code', '')
    if code == '':
        return HttpResponseBadRequest('{"status": 400, "message": "Code is missing"}')
    
    test_cases = TestCases.objects.filter(problem_code=problem_code)
    random_id = str(uuid4())
    curr_dir = str(Path(__file__).resolve().parent)
    inputfile_path = curr_dir+"/tmp/"+random_id+"_input.txt"
    outputfile_path = curr_dir+"/tmp/"+random_id+"_output.txt"
    codefile_path = curr_dir+"/tmp/"+random_id+"_code.cpp"
    passed = False
    generated_output = ""
    cases_passed = 0
    with open(codefile_path, 'w') as fc:
        fc.write(code)
    for t in test_cases:
        with open(inputfile_path, 'w') as fi:
            fi.write(t.input_data)
        with open(outputfile_path, 'w') as fo:
            pass
    
        compiled = os.system('sudo g++ {} -o {}'.format(codefile_path, curr_dir+"/tmp/"+random_id+".out"))
        if compiled != 0:
            os.system('rm -rf {}*'.format(curr_dir+"/tmp/"+random_id))
            return HttpResponse('{"status": 400, "message": "Compilation failed. Check your code"}')
    
        os.system('cat {} | {} | cat > {}'.format(inputfile_path, curr_dir+"/tmp/"+random_id+".out", outputfile_path))

        with open(outputfile_path, 'r') as fo:
            generated_output = fo.read()

        if generated_output.strip() == t.output_data:
            cases_passed+=1

    if cases_passed == len(test_cases):
        new_solution = Solutions(verdict="All Test Cases passed", problem_code=problem_code, problem_id=problem_code, code=code)
        new_solution.save()
        os.system('rm -rf {}*'.format(curr_dir+"/tmp/"+random_id))
        return HttpResponse('{"status": 200, "message": "Passed"}')
    elif cases_passed>0 and cases_passed<len(test_cases):
        new_solution = Solutions(verdict="{} test cases passed out of {}".format(cases_passed, len(test_cases)), problem_code=problem_code, problem_id=problem_code, code=code)
        new_solution.save()
        os.system('rm -rf {}*'.format(curr_dir+"/tmp/"+random_id))
        return HttpResponse('{"status": 200, "message": "Partially Passed"}')
    elif cases_passed == 0:
        os.system('rm -rf {}*'.format(curr_dir+"/tmp/"+random_id))
        return HttpResponse('{"status": 400, "message": "NO test cases passed. Check your code"}')


@csrf_exempt
@require_GET
def leader_board(request):
    solutions = Solutions.objects.all().order_by('-submittedAt')[:10]
    context = {
        'solutions': solutions
    }
    return render(request, 'leaderboard.html', context)


@csrf_exempt
@require_GET
def view_code(request, solid):
    sol = Solutions.objects.filter(id=solid)[0]
    context = {
        'code': sol.code
    }
    return render(request, 'viewcode.html', context)
