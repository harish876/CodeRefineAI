from radon.complexity import cc_visit
from radon.raw import analyze
from radon.metrics import mi_visit,mi_parameters

def analyze_code(code: str):
    # Compute maintainability index
    maintainability_index = mi_visit(code, True)
    print("\nMaintainability Index:", maintainability_index)

    # Compute raw metrics
    raw_metrics = analyze(code)
    print("\nRaw Metrics:")
    print(f" - LOC: {raw_metrics.loc}")
    print(f" - LLOC: {raw_metrics.lloc}")
    print(f" - SLOC: {raw_metrics.sloc}")
    print(f" - Comments: {raw_metrics.comments}")
    print(f" - Multi: {raw_metrics.multi}")
    
    h_volume,c_complexity,lloc,ploc = mi_parameters(code,True)
    print("\nHalstead Volume:", h_volume)
    print("Cyclomatic Complexity:", c_complexity)
    print("Logical Lines of Code:", lloc)
    print("The percent of lines of comment", ploc)


example_code = """
def example_function(n):
    if n < 0:
        return "Negative"
    elif n == 0:
        return "Zero"
    else:
        sum = 0
        for i in range(n):
            sum += i
        return sum
"""

analyze_code(example_code)
