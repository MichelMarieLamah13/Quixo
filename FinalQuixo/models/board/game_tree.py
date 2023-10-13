import threading


class GameTree:
    """
    Cette class represente l'arbre
    """

    def __init__(self, root):
        self.root = root
        current = root
        current.expand()
        threads = []
        if len(current.children) > 0:
            for child in current.children:
                threads.append(threading.Thread(target=GameTree.expand, args=(child,)))
                # child.expand()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def expand(node):
        node.expand()
