import sys

distances = [
    [(1, 15)],
    [(2, 10), (4, 20), (3, 15)],
    [(1, 10), (4, 25), (3, 35)],
    [(1, 15), (4, 30), (2, 35)],
    [(1, 20), (3, 30), (2, 25)],
]


def solve():
    def calculate_best_solution(src: int, total_cities: int):
        visited = set()
        best_solution = sys.maxsize
        best_path = ""

        def DFS(
            src: int,
            starting_city: int,
            cost: int,
            path: str,
            remaining_cities: int,
        ):
            nonlocal best_solution, best_path
            for dest, dist in distances[src]:
                if remaining_cities <= 0 and dest == starting_city:
                    best_solution = min(best_solution, cost + dist)
                    best_path = path + f" -> {dest}"
                    return
                if dest not in visited:
                    visited.add(dest)
                    DFS(
                        dest,
                        starting_city,
                        cost + dist,
                        path + f" -> {dest}",
                        remaining_cities - 1,
                    )
                    visited.remove(dest)
            return

        DFS(src, src, 0, str(src), total_cities - 1)
        return best_solution, best_path

    cities = distances
    min_cost = sys.maxsize
    path: str = ""

    for city in range(0, len(cities)):
        solution = calculate_best_solution(city, len(cities))
        if min_cost > solution[0]:
            min_cost = solution[0]
            path = solution[1]
    print(f"Minimum possible cost is: {min_cost}")
    print(f"Path: {path}")


if __name__ == "__main__":
    solve()
