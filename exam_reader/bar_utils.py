from tqdm import tqdm


class ProcessBar:
    def __init__(self, items, debug=True):
        if debug:
            self.progress_bar = tqdm(
                total=items,
                ascii=" ━",
                bar_format="{percentage:.0f}%|{rate_fmt}|\x1b[31m{bar}\x1b[0m| {n_fmt}/{total_fmt} [{elapsed}<{remaining}",
            )
        self.value = 0
        self.debug = debug

    def __iter__(self):
        return self.progress_bar.__iter__()

    def set_description(self, description):
        if self.debug:
            self.progress_bar.set_description(description)

    def update(self, modify=1):
        if self.debug:
            self.value += modify
            self.progress_bar.update(modify)


__all__ = ["ProcessBar"]
