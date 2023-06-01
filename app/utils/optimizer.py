from scipy.optimize import linprog
import numpy as np

class Optimizer:

    def __init__(self):
        self.prod = [[1 + 0.1 * (j-i) for i in range(1,6)] for j in range(1,6)] 
    
    def prepareData(self, tasks, employees):
        self.tasks = [t.to_lst() for t in tasks]
        self.employees = [e.to_lst() for e in employees]

        if self.tasks and self.employees:
            return True
        return False
    
    def optimize(self, mode="time"):
        n = len(self.employees)
        m = len(self.tasks)
        # Целевая функция: минимизация времени или затра на выполнение проекта
        # where work_ji <-> j = pos // n, i = pos % n
        if mode == "time":
            obj = np.ones(m * n)  
        elif mode == "cost":
            obj = np.array([self.employees[k%n][3] for k in range(m * n)])

        # Ограничения-неравенства, отражающие допутимые лимиты вовлеченности сотрудников
        print("Ограничения-неравенства")
        # Левая часть
        lhs_ineq = np.array([[1 if k % n == i else 0 for k in range(m * n)] for i in range(n)])  
        print(lhs_ineq)
        # Правая часть 
        rhs_ineq = np.array([self.employees[i][2] for i in range(n)])
        print(rhs_ineq)

        # Ограничения-равенства, отражающие завершенность каждой из задач 
        print("Ограничения-равенства")
        # Левая часть
        lhs_eq = np.array([[self.prod[self.tasks[k//n][1]][self.employees[k%n][1]] if k // n == j else 0 for k in range(m * n)] for j in range(m)])
        print(lhs_eq) 
        # Правая часть 
        rhs_eq = np.array([self.tasks[j][2] for j in range(m)])
        print(rhs_eq)
        
        # Естественные ограничения
        bnd = np.array([(0, float("inf")) for _ in range(m * n)]) 
        print(bnd)
        pass

        # Оптимизация
        print("Результат:")
        opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
              method="revised simplex")
        print(opt)

    def showResult(self):
        pass

    def start(self, tasks, employees, mode="time"):
        if self.prepareData(tasks, employees):
            self.optimize(mode=mode)
            self.showResult()

if __name__ == '__main__':
    t = Optimizer()
    for i in range(1,6):
        print(f"Задача {i} сложности: {t.prod[i-1]}")

    t.employees = [[1, 2, 5, 2], [2, 2, 4, 2], [3, 1, 3, 5]]
    t.tasks = [[1, 1, 1], [2, 2, 2], [3, 1, 3], [4, 3, 4]]
    t.optimize()
    t.optimize(mode="cost")
    
    

# # Print the result
# task_assignment = res.x.reshape(-1, num_tasks)
# for i, employee in enumerate(employees.keys()):
#     print(f'{employee} has been assigned tasks: ', end='')
#     for j, task in enumerate(tasks.keys()):
#         if task_assignment[i, j] > 0:
#             print(task, end=', ')
#     print()
