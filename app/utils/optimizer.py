from scipy.optimize import linprog
import numpy as np

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize
class Optimizer:

    def __init__(self):
        self.prod = [[1 + 0.1 * (j-i) for i in range(1,6)] for j in range(1,6)] 
    
    def prepareData(self, tasks, employees):
        self.tasks = [t.to_lst() for t in tasks]
        self.employees = [e.to_lst() for e in employees]

        if self.tasks and self.employees:
            return True
        return False
    
    def optimize(self):
        self.work = np.zeros((len(self.tasks), len(self.employees)))
    
        # Objective function: Minimize total time
        c = np.ones(len(self.tasks) * len(self.employees))        
        pass

    def showResult(self):
        pass

    def start(self, tasks, employees):
        self.prepareData(tasks, employees)
        self.optimize()
        self.showResult()

if __name__ == '__main__':
    t = Optimizer()
    for i in range(1,6):
        print(f"Задача {i} сложности: {t.prod[i-1]}")
    
    print(np.zeros((6, 5)))
    pass
# # Define the employees' working hours and skills
# employees = {
#     '1': (10, 3),
#     '2': (8, 5),
#     '3': (6, 1),
# }

# # Define the tasks' required time and skills
# tasks = {
#     'Task1': (3, 1),
#     'Task2': (4, 1),
#     'Task3': (2, 1),
#     'Task4': (1, 3),
#     'Task5': (3, 5),
# }

# # Build matrix
# num_employees = len(employees)
# num_tasks = len(tasks)
# A = np.zeros((num_employees, num_tasks))
# b = np.array([info[0] for info in employees.values()])

# for i, employee in enumerate(employees.values()):
#     for j, task in enumerate(tasks.values()):
#         if task[1].issubset(employee[1]):
#             A[i, j] = task[0]

# # Objective function: Minimize total time
# c = np.ones(num_tasks)

# # Solve the linear programming problem
# res = linprog(c, A_ub=-A, b_ub=-b, method='highs')

# # Print the result
# task_assignment = res.x.reshape(-1, num_tasks)
# for i, employee in enumerate(employees.keys()):
#     print(f'{employee} has been assigned tasks: ', end='')
#     for j, task in enumerate(tasks.keys()):
#         if task_assignment[i, j] > 0:
#             print(task, end=', ')
#     print()
