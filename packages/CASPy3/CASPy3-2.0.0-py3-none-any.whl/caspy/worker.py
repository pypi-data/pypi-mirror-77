from __future__ import division

from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal, pyqtSlot, QRunnable
from sympy import *
from sympy.abc import _clash1
from sympy.parsing.sympy_parser import parse_expr
import math as m
import cmath as cm

import re as pyreg
from pyperclip import copy


import traceback, sys


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    output = pyqtSignal(dict)


class CASWorker(QRunnable):
    def __init__(self, type, params, copy=None):
        super(CASWorker, self).__init__()

        self.type = type
        self.params = params
        self.copy = copy

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        print(self.type)
        print(self.params)
        print("----")

        try:
            result = getattr(self, self.type)(*self.params)
        except Exception:
            return {"error": f"Error calling function from worker thread: \n{traceback.format_exc()}"}

        # For tests
        if type(result) == list:
            if result[0] == "running":
                self.signals.output.emit({"running": result[1]})
                self.signals.finished.emit()
                return
        if type(result) == str:
            self.signals.output.emit({"answer": result})
            self.signals.finished.emit()
            return

        output = list(result.values())[0]
        if self.copy == 1:
            exact_ans = output[0]
            if type(exact_ans) == list:
                if len(exact_ans) == 1:
                    copy(str(exact_ans[0]))
            else:
                copy(str(exact_ans))
        elif self.copy == 2:
            approx_ans = output[1]
            if type(approx_ans) == list:
                if len(approx_ans) == 1:
                    copy(str(approx_ans[0]))
            else:
                copy(str(approx_ans))
        elif self.copy == 3:
            copy(str(output))
        else:
            pass

        #print(result)
        #copy(str(result))

        self.signals.output.emit(result)
        self.signals.finished.emit()

    # OUTPUTTYPE: 1: PRETTY; 2: LATEX; 3: NORMAL
    # SOLVETYPE: 1: SOLVESET; 2: SOLVE

    @pyqtSlot()
    def is_running(self, to_run):
        return ["running", to_run]

    @pyqtSlot()
    def to_scientific_notation(self, number, accuracy=5):
        """
        Converts number into the string "a*x**b" where a is a float and b is an integer unless it's not a number in the
        complex plane, such as infinity.
        For Complex numbers, a+b*i becomes c*10**d + e*10**f*I

        :param number: str
            number to be converted into
        :param accuracy: int
            accuracy of scientific notation
        :return: str
            scientific notation of number in string
        """

        # Is "a+b*i -> c*10**d + e*10**f*I" even a thing?
        # Can't find anything on internet but I'm implementing it like this for now

        number = str(number)
        sym_num = sympify(number)

        if not sym_num.is_complex:
            return number

        if type(accuracy) != int:
            print("Accuracy must be an integer over 1, defaulting to 5")
            accuracy = 5

        if accuracy < 1:
            print("Accuracy must be an integer over 1, defaulting to 5")
            accuracy = 5

        if sym_num.is_real:

            if sym_num < 0:
                negative = "-"
                number = number[1:]
                sym_num = sympify(number)
            else:
                negative = ""

            int_part = number.split(".")[0]
            no_decimal = number.replace(".", "")

            # convert it into 0.number, round it then convert it back into number
            output = str(sympify("0." + no_decimal).round(accuracy))[2:]
            if accuracy != 1:
                output = output[:2] + "." + output[2:]

            if sym_num < 1:
                zero_count = 0
                while zero_count < len(no_decimal) and no_decimal[zero_count] == "0":
                    zero_count += 1

                output = no_decimal[zero_count:]
                output = str(sympify("0." + output).round(accuracy))[2:]

                if accuracy != 1:
                    output = output[:1] + "." + output[1:]

                output += f"*10**(-{zero_count})"
                return negative + output
            else:
                output = str(sympify("0." + no_decimal).round(accuracy))[2:]
                if accuracy != 1:
                    output = output[:1] + "." + output[1:]

                output += "*10**" + str(len(int_part.replace("-", "")) - 1)
                return negative + output
        else:
            real = re(sym_num)
            imag = im(sym_num)

            real = self.to_scientific_notation(real, accuracy)
            imag = self.to_scientific_notation(imag, accuracy)

            output = real
            if sympify(imag) < 0:
                output += f" - {imag[1:]}*I"
            else:
                output += f" + {imag}*I"
            return output

    @pyqtSlot()
    def prev_deriv(self, input_expression, input_variable, input_order, input_point, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            derivative = Derivative(str(input_expression), input_variable, input_order)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(derivative))

        if input_point:
            self.exact_ans = f"At {input_variable} = {input_point}\n"

        if output_type == 1:
            self.exact_ans += str(pretty(derivative))
        elif output_type == 2:
            self.exact_ans += str(latex(derivative))
        else:
            self.exact_ans += str(derivative)

        return {"deriv": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_deriv(self, input_expression, input_variable, input_order, input_point, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            self.exact_ans = diff(parse_expr(input_expression), parse_expr(input_variable), input_order)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if input_point:
            calc_deriv_point = str(self.exact_ans).replace(input_variable, f"({input_point})")

            if use_scientific:
                self.approx_ans = self.to_scientific_notation(str(N(calc_deriv_point, accuracy)), use_scientific)
            else:
                self.approx_ans = str(N(calc_deriv_point, accuracy))

            self.latex_answer = str(latex(simplify(calc_deriv_point)))
            if output_type == 1:
                self.exact_ans = str(pretty(simplify(calc_deriv_point)))
            elif output_type == 2:
                self.exact_ans = str(latex(simplify(calc_deriv_point)))
            else:
                self.exact_ans = str(simplify(calc_deriv_point))
        else:
            if output_type == 1:
                self.exact_ans = str(pretty(self.exact_ans))
            elif output_type == 2:
                self.exact_ans = str(latex(self.exact_ans))
            else:
                self.exact_ans = str(self.exact_ans)

        return {"deriv": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_integ(self, input_expression, input_variable, input_lower, input_upper, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return {"error": ["Enter both upper and lower bound"]}

        if input_lower:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), (parse_expr(input_variable),
                                                                         input_lower, input_upper))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            try:
                self.exact_ans = Integral(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(self.exact_ans))
        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"integ": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_integ(self, input_expression, input_variable, input_lower, input_upper, approx_integ, output_type,
                   use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}
        if (input_lower and not input_upper) or (not input_lower and input_upper):
            return {"error": ["Enter both upper and lower bound"]}

        if input_lower:
            try:
                self.exact_ans = Integral(parse_expr(input_expression),
                                          (parse_expr(input_variable), input_lower, input_upper))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            if approx_integ:
                self.exact_ans = N(self.exact_ans, accuracy)
            else:
                try:
                    self.exact_ans = self.exact_ans.doit()
                except Exception:
                    return {"error": [f"Error: \n{traceback.format_exc()}"]}

            self.latex_answer = str(latex(self.exact_ans))

            try:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(simplify(N(self.exact_ans, accuracy)))
            except Exception:
                self.approx_ans = 0
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            else:
                if use_scientific:
                    self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
                else:
                    self.approx_ans = str(N(self.exact_ans, accuracy))

        else:
            try:
                self.exact_ans = integrate(parse_expr(input_expression), parse_expr(input_variable))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"integ": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_limit(self, input_expression, input_variable, input_approach, input_side, output_type,
                   use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_approach:
            return {"error": ["Enter value that the variable approaches"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            self.exact_ans = Limit(parse_expr(input_expression), parse_expr(input_variable), input_approach, input_side)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)


        return {"limit": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_limit(self, input_expression, input_variable, input_approach, input_side, output_type,
                   use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not input_expression:
            return {"error": ["Enter an expression"]}
        if not input_approach:
            return {"error": ["Enter value that the variable approaches"]}
        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            self.exact_ans = limit(parse_expr(input_expression), parse_expr(input_variable), input_approach, input_side)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if use_scientific:
            self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
        else:
            self.approx_ans = str(N(self.exact_ans, accuracy))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"limit": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_normal_eq(self, left_expression, right_expression, input_variable, domain,
                       output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                left_expression = eq[0]
                right_expression = eq[1]
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

        if not input_variable:
            return {"error": ["Enter a variable"]}

        try:
            full_equation = Eq(parse_expr(left_expression), parse_expr(right_expression))
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(full_equation))

        if output_type == 1:
            self.exact_ans = str(pretty(full_equation))
        elif output_type == 2:
            self.exact_ans = self.latex_answer
        else:
            self.exact_ans = str(full_equation)

        self.exact_ans += f"\nDomain: {domain}"

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_diff_eq(self, left_expression, right_expression, function_solve, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)

        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                try:
                    left_side = parse_expr(self.parse_diff_text(eq[0]))
                    right_side = parse_expr(self.parse_diff_text(eq[1]))
                except Exception:
                    return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

            try:
                left_side = parse_expr(self.parse_diff_text(left_expression))
                right_side = parse_expr(self.parse_diff_text(right_expression))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if not function_solve:
            return {"error": ["Enter a function to solve for"]}

        try:
            full_equation = Eq(left_side, right_side)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(full_equation))

        if output_type == 1:
            self.exact_ans = str(pretty(full_equation))
        elif output_type == 2:
            self.exact_ans = self.latex_answer
        else:
            self.exact_ans = str(full_equation)

        try:
            self.exact_ans += f"\nClassification: {str(classify_ode(full_equation))}"
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_system_eq(self, equations, variables, domain, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        equations = self.get_equations(equations)
        if equations[0] == "error":
            return {"error": [f"Error: \nEnter only one '=' on line {equations[1] + 1}"]}

        variables = self.get_vars(variables)
        if variables[0] == "error":
            return {"error": [f"Error: \n{variables[1]}"]}

        self.latex_answer = str(latex(equations))
        if output_type == 1:
            self.exact_ans = str(pretty(equations))
        elif output_type == 2:
            self.exact_ans = str(latex(equations))
        else:
            self.exact_ans = str(equations)

        self.exact_ans += f"\nDomain: {domain}"

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_normal_eq(self, left_expression, right_expression, input_variable, solve_type, domain,
                       output_type, use_unicode, line_wrap, use_scientific, accuracy, verify_domain):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        try:
            domain = parse_expr(domain)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                left_expression = eq[0]
                right_expression = eq[1]
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

        if not input_variable:
            return {"error": ["Enter a variable"]}

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if solve_type == 1: # 1: solveset, 2: solve
            try:
                self.exact_ans = solveset(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable), domain=domain)
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

        else:
            try:
                self.exact_ans = solve(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable), domain=domain)
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            if verify_domain:
                self.exact_ans = self.verify_domain(self.exact_ans, domain)

            approx_list = [N(i, accuracy) for i in self.exact_ans]
            if use_scientific:
                approx_list = [self.to_scientific_notation(str(i), use_scientific) for i in approx_list]

            self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        self.latex_answer = str(latex(self.exact_ans))
        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_diff_eq(self, left_expression, right_expression, hint, function_solve,
                     output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if "=" in left_expression:
            if left_expression.count("=") > 1:
                return {"error": ["Enter only one equals sign"]}
            else:
                eq = left_expression.split("=")
                left_side = parse_expr(self.parse_diff_text(eq[0]))
                right_side = parse_expr(self.parse_diff_text(eq[1]))
        else:
            if not left_expression or not right_expression:
                return {"error": ["Enter an expression both in left and right side"]}

            left_side = parse_expr(self.parse_diff_text(left_expression))
            right_side = parse_expr(self.parse_diff_text(right_expression))

        if not function_solve:
            return {"error": ["Enter a function"]}

        if not hint:
            hint = 'default'

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        diffeq = Eq(left_side, right_side)
        self.exact_ans = dsolve(diffeq, parse_expr(function_solve), hint=hint)
        self.latex_answer = str(latex(self.exact_ans))

        approx_list = [N(i, accuracy) for i in self.exact_ans]
        if use_scientific:
            approx_list = [self.to_scientific_notation(str(i), use_scientific) for i in approx_list]

        self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
            self.approx_ans = str(pretty(self.approx_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
            self.approx_ans = str(latex(self.approx_ans))
        else:
            pass

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_system_eq(self, equations, variables, domain, output_type,
                       use_unicode, line_wrap, use_scientific, accuracy, verify_domain):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        equations = self.get_equations(equations)
        if equations[0] == "error":
            return {"error": [f"Error: \nEnter only one '=' on line {equations[1] + 1}"]}

        variables = self.get_vars(variables)
        if variables[0] == "error":
            return {"error": [f"Error: \n{variables[1]}"]}

        try:
            domain = parse_expr(domain)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        try:
            result = solve(equations, variables)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if verify_domain:
            temp_result = []
            for i in result:
                if not(False in [j in domain for j in i]):
                    temp_result.append(i)

            result = temp_result

        try:
            output = []
            self.approx_ans = []
            for i in range(len(result)):
                temp_output = []
                temp_approx_output = []
                for j in range(len(variables)):
                    approx_ans = N(result[i][j], accuracy)
                    print(approx_ans)
                    if use_scientific:
                        approx_ans = self.to_scientific_notation(str(approx_ans), use_scientific)

                    temp_approx_output.append(f"{variables[j]} = {approx_ans}")
                    temp_output.append(Eq(variables[j], result[i][j]))
                output.append(temp_output)
                self.approx_ans.append(temp_approx_output)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        self.latex_answer = str(latex(output))

        if output_type == 1:
            self.exact_ans = str(pretty(output))
        elif output_type == 2:
            self.exact_ans = self.latex_answer
        else:
            self.exact_ans = str(output)

        return {"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def get_equations(self, equations):
        """
        Each equation is to be typed as 'expr1 = expr2'.
        This checks that exactly one '=' is present and if not, show error box and return "error"
        :param equations: list
            List of all equations as strings
        :return: list
            Returns list of SymPy Eq()
        """
        eq = []
        for line in equations:
            if line.count("=") != 1:
                return ["error", equations.index(line)]
            line_equal = line.split("=")
            eq.append(Eq(parse_expr(line_equal[0]), parse_expr(line_equal[1])))
        return eq

    @pyqtSlot()
    def get_vars(self, var_text):
        """
        Return vars that is separated by anything other than a-z, 0-9, and _
        :param var_text: str
            Text of QLineEdit
        :return: list
            Returns list of SymPified symbols
        """

        var_re = pyreg.compile(r"[a-zA-Z0-9_]+")
        vars = var_re.findall(var_text)
        output = []
        for var in vars:
            try:
                output.append(parse_expr(var))
            except Exception:
                return ["error", traceback.format_exc()]
        if not output:
            return ["error", "Please enter at least one variable"]
        return output

    @pyqtSlot()
    def verify_domain(self, input_values, domain):
        output = []
        for value in input_values:
            if value in domain:
                output.append(value)

        return output

    @pyqtSlot()
    def parse_diff_text(self, text):
        """
        Catches all derivatives and transforms it so SymPy can read it.
        No nested functions because no.
        Function already in SymPy syntax (Ex. 'f(x).diff(x,3)') will be ignored.
        Examples (Not what function will return, just how it transforms functions)
            f'''(x)
            => f(x).diff(x,3)

            f''(x, y, z)
            => f(x, y, z).diff(x,2,y,2,z,2)

        :param text: str
            String to be parsed
        :return: str
            String with transformed derivatives
        """

        diff_functions = pyreg.compile(r"(?:[a-zA-Z])+('+)\(.*?\)")
        inside_params = pyreg.compile(r"(?<=\().+?(?=\))")
        quotations = pyreg.compile(r"'+(?=\()")

        functions = diff_functions.finditer(text)

        for function in functions:
            output = ""
            func_str = function.group(0)
            inside_param = inside_params.search(func_str).group(0)
            order = len(function.group(1))
            function_no_order = quotations.sub("", func_str)

            inside_param = inside_param.strip(" ")
            vars = [i.strip() for i in inside_param.split(",")]

            output += f"{function_no_order}.diff("
            for var in vars:
                output += f"{var},{order},"

            output = output[:-1]
            output += ")"

            text = text.replace(func_str, output)

        return text

    r'''
    @pyqtSlot()
    def prev_eq(self, left_expression, right_expression, input_variable,
                output_text, output_type, use_unicode, line_wrap, cli=False):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = "\\text{LaTeX support not yet implemented for equation}"

        if not left_expression or not right_expression:
            return {"error": ["Enter an expression both in left and right side"]}

        if not input_variable:
            return {"error": ["Enter a variable"]}

        if output_type == 1:
            """
            Since Pretty will be multiline, left and right side is broken up to not mess up equals symbol.
            Toggles between
            """
            if cli:
                eq_to_out = "Left side:\n\n"
                try:
                    eq_to_out += str(pretty(parse_expr(left_expression)))
                except Exception:
                    return ({"error": [f"Error: \n{traceback.format_exc()}"]})
                eq_to_out += "\n\nRight Side:\n\n"
                try:
                    eq_to_out += str(pretty(parse_expr(right_expression)))
                except Exception:
                    return ({"error": [f"Error: \n{traceback.format_exc()}"]})
                self.exact_ans = eq_to_out

            else:
                if output_text == "" or output_text[0:10] == "Right side":
                    eq_to_out = "Left side, click again for right side\n"
                    try:
                        eq_to_out += str(pretty(parse_expr(left_expression)))
                    except Exception:
                        return({"error": [f"Error: \n{traceback.format_exc()}"]})
                    self.exact_ans = eq_to_out
                else:
                    eq_to_out = "Right side, click again for left side\n"
                    try:
                        eq_to_out += str(pretty(parse_expr(right_expression)))
                    except Exception:
                        return({"error": [f"Error: \n{traceback.format_exc()}"]})
                    self.exact_ans = eq_to_out

        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(left_expression))) + " = " + str(latex(parse_expr(right_expression)))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
        else:
            self.exact_ans = str(left_expression) + " = " + str(right_expression)

        return({"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer})

    @pyqtSlot()
    def calc_eq(self, left_expression, right_expression, input_variable, solve_type, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = "\\text{LaTeX support not yet implemented for equation}"

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not left_expression or not right_expression:
            return ({"error": ["Enter an expression both in left and right side"]})

        if not input_variable:
            return ({"error": ["Enter a variable"]})

        if solve_type == 1: # 1: solveset, 2: solve
            try:
                self.exact_ans = solveset(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
            self.approx_ans = 0
        else:
            try:
                self.exact_ans = solve(Eq(parse_expr(left_expression), parse_expr(right_expression)), parse_expr(input_variable))
            except Exception:
                return({"error": [f"Error: \n{traceback.format_exc()}"]})
            approx_list = [N(i, accuracy) for i in self.exact_ans]
            if use_scientific:
                approx_list = [self.to_scientific_notation(str(i), use_scientific) for i in approx_list]

            self.approx_ans = approx_list[0] if len(approx_list) == 1 else approx_list

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return({"eq": [self.exact_ans, self.approx_ans], "latex": self.latex_answer})
    '''

    @pyqtSlot()
    def prev_simp_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            self.latex_answer = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(expression)
        self.latex_answer = str(latex(parse_expr(expression, evaluate=False)))

        return {"simp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def simp_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        try:
            self.exact_ans = simplify(expression)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"simp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_expand_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        if output_type == 1:
            try:
                self.exact_ans = str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        elif output_type == 2:
            try:
                self.exact_ans = str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
            self.latex_answer = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(expression)
        self.latex_answer = str(latex(parse_expr(expression, evaluate=False)))

        return {"exp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def expand_exp(self, expression, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expressiobn"]}

        try:
            self.exact_ans = expand(expression)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"exp": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def prev_eval_exp(self, expression, var_sub, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if not expression:
            return {"error": ["Enter an expression"]}

        if var_sub:
            self.exact_ans = f"With variable substitution {var_sub}\n"

        self.latex_answer = str(latex(parse_expr(expression, evaluate=False)))
        if output_type == 1:
            try:
                self.exact_ans += str(pretty(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        elif output_type == 2:
            try:
                self.exact_ans += str(latex(parse_expr(expression, evaluate=False)))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}
        else:
            self.exact_ans += str(expression)

        return {"eval": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def parse_var_sub(self, var_sub):
        """
        Parses var_sub and returns a dictionary. Any variable followed by a ':' will be subtituted by everything
        between the ':' and the next variable. It must be of the type var1: value1 var2: value2 or else
        it will return an error

        Examples:
            t: 34 y: pi/3 z: 5
            => {'t': '34', 'y': 'pi/3', 'z': '5'}

        :param var_sub: string
            String containing variables
        :return: Dict
            Dictionary with variable as key and subtition as value
        """
        match_key = pyreg.compile(r"[a-zA-Z0-9_]+:")
        output = {}

        key_reg = match_key.finditer(var_sub)
        keys = [i.group(0) for i in key_reg]

        for key in range(len(keys) - 1):
            start = keys[key]
            end = keys[key+1]
            in_between = pyreg.compile(f"{start}(.*){end}")

            result = in_between.search(var_sub).group(1).strip()
            if not result:
                return {"error": f"Variable '{start[0:-1]}' is missing a value"}

            output[start[0:-1]] = result

        last_value = var_sub.split(keys[-1])[1].strip()
        if not last_value:
            return {"error": f"Variable '{keys[-1][0:-1]}' is missing a value"}
        output[keys[-1][0:-1]] = last_value

        print(output)
        return output

    @pyqtSlot()
    def eval_exp(self, expression, var_sub, output_type, use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        self.approx_ans = 0
        self.exact_ans = ""
        self.latex_answer = ""

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        if not expression:
            return {"error": ["Enter an expression"]}

        if var_sub:
            if ":" not in var_sub:
                return {"error": ["A ':' must be present after variable to indicate end of variable"]}

            var_sub = self.parse_var_sub(var_sub)
            if "error" in list(var_sub.keys()):
                return {"error": [var_sub["error"]]}

            for var in var_sub.keys():
                expression = expression.replace(var, f"({var_sub[var]})")

        try:
            self.exact_ans = simplify(parse_expr(expression))
            if use_scientific:
                self.approx_ans = self.to_scientific_notation(str(N(self.exact_ans, accuracy)), use_scientific)
            else:
                self.approx_ans = str(N(self.exact_ans, accuracy))
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}
        self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"eval": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_pf(self, input_number):
        self.approx_ans = ""
        self.latex_answer = ""

        try:
            input_number = int(input_number)
        except:
            return {"error": [f"Error: {input_number} is not an integer."]}

        if input_number < 1:
            return {"error": [f"Error: {input_number} is lower than 1, only number 1 and above is accepted."]}

        try:
            self.exact_ans = factorint(input_number)
        except Exception:
            return {"error": [f"Error: \n{traceback.format_exc()}"]}

        for base in self.exact_ans:
            self.latex_answer += f"({base}**{self.exact_ans[base]})*"
            self.approx_ans += f"({base}**{self.exact_ans[base]})*"

        self.latex_answer = latex(parse_expr(self.latex_answer[0:-1], evaluate=False))
        return {"pf": [self.exact_ans, self.approx_ans[0:-1]], "latex": self.latex_answer}

    @pyqtSlot()
    def execute_code(self, code, namespace):
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = r"\text{LaTeX not supported for shell}"
        new_namespace = namespace

        class Capturing(list):
            from io import StringIO
            def __enter__(self):
                self._stdout = sys.stdout
                sys.stdout = self._stringio = self.StringIO()
                return self

            def __exit__(self, *args):
                self.extend(self._stringio.getvalue().splitlines())
                del self._stringio
                sys.stdout = self._stdout

        try:
            with Capturing() as self.output:
                try:
                    exec(f"print({code})", namespace)
                except Exception:
                    exec(code, namespace)
        except Exception:
            self.output = f"\nError: {traceback.format_exc()}"

        new_namespace.update(locals())

        if type(self.output) != str:
            for i in self.output:
                self.exact_ans += f"{i}\n"

            self.exact_ans = self.exact_ans[:-1]
        else:
            self.exact_ans = self.output

        return {"exec": [self.exact_ans, self.approx_ans], "latex": self.latex_answer, "new_namespace": new_namespace}

    @pyqtSlot()
    def prev_formula(self, lines, value_string, output_type, use_unicode, line_wrap):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = ""

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(empty_var_list) > 1 and len(var_list) != 1:
            return {"error": ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}

        left_side = value_string[0]
        right_side = value_string[1]

        self.exact_ans = Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1))
        self.latex_answer = str(latex(self.exact_ans))

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"formula": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}

    @pyqtSlot()
    def calc_formula(self, lines, value_string, solve_type, output_type,
                     use_unicode, line_wrap, use_scientific, accuracy):
        init_printing(use_unicode=use_unicode, wrap_line=line_wrap)
        empty_var_list, var_list, values = [], [], []
        self.exact_ans = ""
        self.approx_ans = 0
        self.latex_answer = "\\text{LaTeX support not yet implemented for formula}"

        if use_scientific:
            if use_scientific > accuracy:
                accuracy = use_scientific

        for line in lines:
            if line[0].text() == "":
                empty_var_list.append(line[1])
            elif line[0].text() == "var":
                var_list.append(line[1])
            else:
                values.append([line[0].text(), line[1]])

        if len(empty_var_list) > 1 and len(var_list) != 1:
            return {"error": ["Solve for only one variable, if multiple empty lines type 'var' to solve for the variable"]}

        if len(var_list) == 1:
            final_var = var_list[0]
        else:
            final_var = empty_var_list[0]

        left_side = parse_expr(value_string[0])
        right_side = parse_expr(value_string[1])

        for i in values:
            left_side = left_side.subs(parse_expr(i[1]), i[0])
            right_side = right_side.subs(parse_expr(i[1]), i[0])

        left_side = str(left_side).replace("_i", "(sqrt(-1))")
        right_side = str(right_side).replace("_i", "(sqrt(-1))")

        if solve_type == 2:
            try:
                self.exact_ans = solve(Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1)), parse_expr(final_var, _clash1))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            self.approx_ans = list(map(lambda x: N(x, accuracy), self.exact_ans))
            if len(self.approx_ans) == 1:
                self.approx_ans = self.approx_ans[0]

            if use_scientific:
                if type(self.approx_ans) == 'list':
                    self.approx_ans = list(map(lambda x: self.to_scientific_notation(str(x), use_scientific), self.approx_ans))
                else:
                    self.approx_ans = self.to_scientific_notation(str(self.approx_ans), use_scientific)

        else:
            try:
                self.exact_ans = solveset(Eq(parse_expr(left_side, _clash1), parse_expr(right_side, _clash1)), parse_expr(final_var, _clash1))
            except Exception:
                return {"error": [f"Error: \n{traceback.format_exc()}"]}

            self.approx_ans = 0

        if output_type == 1:
            self.exact_ans = str(pretty(self.exact_ans))
        elif output_type == 2:
            self.exact_ans = str(latex(self.exact_ans))
        else:
            self.exact_ans = str(self.exact_ans)

        return {"formula": [self.exact_ans, self.approx_ans], "latex": self.latex_answer}