from django.urls import path
from .views import home,index,view_problem,evaluate_code,leader_board,view_code

urlpatterns = [
    path('problems/', index),
    path('problems/<int:page>', home),
    path('problem/<code>', view_problem),
    path('problem/<code>/submit', evaluate_code),
    path('problems/leaderboard', leader_board),
    path('problem/viewcode/<solid>', view_code)
]
