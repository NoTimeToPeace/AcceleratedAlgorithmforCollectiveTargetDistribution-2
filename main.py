import random
import numpy as np


class Target:
    def __init__(self):
        self.__complexity = random.uniform(1, 10)
        self.__isReady = False
        self.__N_max = random.randint(1, 3)

    def changeComplexity(self, performance):
        if self.__complexity > 0:
            self.__complexity = self.__complexity - performance
        else:
            self.__isReady = True

    def getComplexity(self):
        return self.__complexity

    def getN_max(self):
        return self.__N_max

    def isReady(self):
        return self.__isReady


class Robot:
    def __init__(self, numberOfTargets):
        self.__powerD = np.array([random.random() for i in range(numberOfTargets)])
        self.__free = True
        self.__target = None
        self.__powerUsed = 0
        self.efficientD = None

    def setTarget(self, target, power):
        if self.__target is None and self.isFree():
            self.__target = target
            self.__powerUsed = power
            self.setEmployment()

    def resetTarget(self):
        self.__target = None
        self.__free = True
        self.__powerUsed = 0

    def isFree(self):
        return self.__free

    def getPowerD(self):
        return self.__powerD

    def getPowerUsed(self):
        return self.__powerUsed

    def setEmployment(self):
        self.__free = not self.__free

    def getTarget(self):
        return self.__target


# Обновление матрицы D
def UpdateMatrixD(D, N_max, robots, targets):
    for i in range(0, len(robots)):
        if robots[i].isFree():
            D[i] = robots[i].getPowerD()

    for i in range(0, len(targets)):
        if targets[i].isReady() or N_max[i] == 0:
            D[:, i] = 0


# Вывод матрицы D и N_max
def printMatrix_D_N_max(D, N_max):
    print("\nМатрица D:")
    print(D)
    print("\nВектор N_max:")
    print(N_max)


# Определение номера задачи
def findPositionTarget(targets, robot):
    for x in range(len(targets)):
        if targets[x] == robot.getTarget():
            return x


def algorithm():
    targets = np.array([Target() for i in range(random.randint(1, 15))])  # Создаём цели от 1 до 15
    robots = np.array([Robot(len(targets)) for i in range(random.randint(1, 15))])  # Создаём роботов от 1 до 15
    D = np.vstack([i.getPowerD() for i in robots])  # Получаем общую матрицу эффективности роботов над задачами
    N_max = np.array([i.getN_max() for i in
                      targets])  # Получаем общий вектор максимально возможного количества роботов, работающих над задачей

    print("Количество роботов: " + str(len(robots)) + "\nКоличество целей: " + str(len(targets)))
    printMatrix_D_N_max(D, N_max)

    # Пока все цели не выполнены, пытаемся их выполнить
    while not all([x.isReady() for x in targets]):
        # Распределение целей между роботами
        for i in range(0, len(robots)):
            # Проверяем, необходимо ли распределять цели между роботами
            if np.all(D <= 0.0001) or np.all(N_max <= 0.0001):
                print("\nМатрица D или N_max содержат все нули")
                break
            else:
                if robots[i].isFree():
                    print("\nРаспределение целей между свободными роботами")
                    col = np.argmax(D[i]) # Находим максимальное значение эффективности для робота
                    row = np.argmax(D[:, col]) # Находим лучшее значение эффиктивности среди всех роботов по выбранной задаче

                    copyD = np.copy(robots[i].getPowerD())
                    np.put(copyD, col, 0) # Нулим максимальное значение в копии
                    # Если остался осталась всего одна невыполненная цель
                    if (np.all(copyD <= 0.0001)):
                        robots[i].efficientD = 0
                    else:
                        # Ищем дельту эффективности относительно других целей
                        robots[i].efficientD = D[i][col] - D[i][np.argmax(copyD)]

                    # Если у всех роботов вычислился коэффициент дельта d, то распределяем цели
                    if (np.all(np.array([robots[pepe].efficientD != None for pepe in range(0, len(robots))]) == True)):
                        print(str(robots[-1].efficientD))
                        return





if __name__ == '__main__':
    np.set_printoptions(precision=2, floatmode='fixed')
    np.set_printoptions(threshold=np.inf)
    algorithm()