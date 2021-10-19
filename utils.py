def run_task_with_retries(func, args, max_retries=3):
    while True:
        try:
            return func(*args)
        except Exception as e:
            if max_retries == 0:
                return None
            print(f"{max_retries} Error running task {func.__name__}: {e} Retrying")
            max_retries -= 1
