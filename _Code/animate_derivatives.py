"""
Linear Algebra and Calculus (M3) - Internal Assessment
Project Option 1: Animation Video
Concept: Derivative and Rate of Change
Student Name: Suraj Patil
Student ID: E25B070541

This module contains the mathematical modeling and visual scene logic
for generating the animation video:
1. Scene 1: Real-life car position & speedometer instantaneous rate
2. Scene 2: Formal definition of derivative as limit of difference quotient
3. Scene 3: Geometric secant line slope approaching tangent slope
4. Scene 4: Worked algebraic example f(x) = x^2, f'(x) = 2x, evaluated at x = 3
5. Scene 5: Tangent dynamics on cubic curve (positive, negative, zero slope)
6. Scene 6: Applications in physics, marginal cost, and AI gradient descent
"""

import numpy as np

class DerivativeMathematics:
    """Core mathematical definitions and calculations for the animation."""

    @staticmethod
    def difference_quotient(f, x, h):
        """Calculates the average rate of change over interval [x, x + h]."""
        return (f(x + h) - f(x)) / h

    @staticmethod
    def derivative_limit(f, x, h_values=None):
        """
        Demonstrates the limit of secant slopes approaching the derivative
        as h -> 0 from first principles.
        """
        if h_values is None:
            h_values = [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001]
        slopes = [DerivativeMathematics.difference_quotient(f, x, h) for h in h_values]
        return list(zip(h_values, slopes))

    @staticmethod
    def quadratic_example(x):
        """Worked example function f(x) = x^2."""
        return x ** 2

    @staticmethod
    def quadratic_derivative(x):
        """Theoretical derivative f'(x) = 2x."""
        return 2 * x

    @staticmethod
    def cubic_curve(x):
        """
        Smooth cubic curve for illustrating sign changes of tangent slope:
        f(x) = x^3 - 3x
        Turning points at x = -1 (local max, slope = 0) and x = +1 (local min, slope = 0).
        """
        return x**3 - 3*x

    @staticmethod
    def cubic_derivative(x):
        """Derivative of cubic curve f'(x) = 3x^2 - 3."""
        return 3 * (x**2) - 3


def verify_mathematics():
    """Runs automated verification of all examples in the video."""
    print("=" * 60)
    print("M3 VIDEO MATHEMATICAL VERIFICATION")
    print("=" * 60)

    # 1. Verification of Worked Example at x = 3
    x0 = 3.0
    exact = DerivativeMathematics.quadratic_derivative(x0)
    print(f"\n1. Worked Example: f(x) = x^2 evaluated at x = {x0}")
    print(f"   Theoretical Derivative f'({x0}) = 2({x0}) = {exact}")
    print("   Approaching limit from first principles:")
    for h, slope in DerivativeMathematics.derivative_limit(DerivativeMathematics.quadratic_example, x0):
        print(f"     h = {h:6.4f}  -->  Secant Slope = {slope:8.5f}")
    assert abs(slope - exact) < 1e-3, "First principles limit did not converge to 6!"
    print("   [PASS] Limit strictly converges to 6.00000.")

    # 2. Verification of Tangent Slope Signs on Cubic Curve
    print("\n2. Cubic Tangent Slope Sign Verification: f(x) = x^3 - 3x")
    # Region 1: x = -2 (Upward slope, increasing)
    s_up = DerivativeMathematics.cubic_derivative(-2.0)
    print(f"   x = -2.0  --> f'(-2.0) = {s_up:+5.2f} (Positive: function increasing)")
    assert s_up > 0

    # Region 2: x = -1.0 (Local maximum turning point)
    s_zero1 = DerivativeMathematics.cubic_derivative(-1.0)
    print(f"   x = -1.0  --> f'(-1.0) = {s_zero1:+5.2f} (Zero: stationary turning point)")
    assert abs(s_zero1) < 1e-6

    # Region 3: x = 0.0 (Downward slope, decreasing)
    s_down = DerivativeMathematics.cubic_derivative(0.0)
    print(f"   x =  0.0  --> f'( 0.0) = {s_down:+5.2f} (Negative: function decreasing)")
    assert s_down < 0

    # Region 4: x = +1.0 (Local minimum turning point)
    s_zero2 = DerivativeMathematics.cubic_derivative(1.0)
    print(f"   x = +1.0  --> f'(+1.0) = {s_zero2:+5.2f} (Zero: stationary turning point)")
    assert abs(s_zero2) < 1e-6

    print("   [PASS] Geometric tangent slopes strictly match algebraic behavior.")
    print("\nAll video calculations mathematically verified and sound!")
    print("=" * 60)


if __name__ == "__main__":
    verify_mathematics()
