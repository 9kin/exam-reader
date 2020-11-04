from tqdm import tqdm


class Bar:
    def __init__(self, items, debug=True):
        if debug:
            self.bar = tqdm(
                total=items,
                ascii=" ━",
                bar_format="{percentage:.0f}%|{rate_fmt}|\x1b[31m{bar}\x1b[0m| {n_fmt}/{total_fmt} [{elapsed}<{remaining}",
            )
        self.val = 0
        self.debug = debug

    def __iter__(self):
        return self.bar.__iter__()

    def set_description(self, s):
        if self.debug:
            self.bar.set_description(s)

    def update(self, n=1):
        if self.debug:
            self.val += n
            self.bar.update(n)


__all__ = ["Bar"]
