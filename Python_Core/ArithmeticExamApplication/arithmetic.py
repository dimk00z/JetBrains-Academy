from random import choice, randint


class MiniCalculator:
    def __init__(self):
        self.operations = {
            "+": MiniCalculator.addition,
            "-": MiniCalculator.subtraction,
            "*": MiniCalculator.multiplication,
        }

    @staticmethod
    def addition(*numbers):
        return sum(numbers)

    @staticmethod
    def subtraction(*numbers):
        result = numbers[0]
        for num in numbers[1:]:
            result = result - num
        return result

    @staticmethod
    def multiplication(*numbers):
        result = numbers[0]
        for num in numbers[1:]:
            result = result * num
        return result

    @staticmethod
    def square(num):
        return num * num

    def calculate(self, line, level: int = 1):

        if level == 2:
            return MiniCalculator.square(int(line))

        num1, operation, num2 = line.split()
        num1, num2 = map(int, (num1, num2))
        if operation in self.operations:
            return self.operations[operation](num1, num2)

    def generate_math_task(self, level: int = 1):
        levels = {1: (2, 9), 2: (11, 29)}
        random_operation = choice(tuple(self.operations))
        random_nums = (randint(*levels[level]), randint(*levels[level]))
        if level == 1:
            math_task = f"{random_nums[0]} {random_operation} {random_nums[1]}"
        else:
            math_task = f"{random_nums[0]}"
        return math_task

    @staticmethod
    def get_int_input():
        while True:
            user_input = input()
            try:
                int(user_input)
                return user_input
            except ValueError:
                print("Incorrect format.")

    def user_check(self, tasks=5):
        levels = {
            1: "simple operations with numbers 2-9",
            2: "integral squares of 11-29",
        }
        print(
            "\n".join(
                (
                    "Which level do you want? Enter a number:",
                    f"1 - {levels[1]}",
                    f"2 - {levels[2]}",
                )
            )
        )
        level = MiniCalculator.get_int_input()

        result = 0
        for _ in range(tasks):
            math_task = self.generate_math_task(level=int(level))
            print(math_task)
            user_input = MiniCalculator.get_int_input()
            if user_input == str(self.calculate(line=math_task, level=int(level))):
                print("Right!")
                result += 1
            else:
                print("Wrong!")

        print(
            f"Your mark is {result}/{tasks}.Would you like to save the result? Enter yes or no."
        )
        user_answer = input()
        if user_answer.lower() in ("yes", "y"):
            user_name = input("What is your name?\n")
            with open("results.txt", mode="a+", encoding="utf-8") as file:
                file.write(
                    f"{user_name}: {result}/{tasks} in level {level} ({levels[int(level)]})\n"
                )
            print('The results are saved in "results.txt".')


if __name__ == "__main__":
    mini_calc = MiniCalculator()
    mini_calc.user_check()
