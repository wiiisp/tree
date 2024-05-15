class Noeud:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = Noeud()

    # Insertion dun nouveau mot
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                # Instancie un nouveau noeud a chaque nouveau caractère du mot
                node.children[char] = Noeud()
            # le nouveau noeud est le nouveau root pour la prochaine iteration
            node = node.children[char]
        node.is_end_of_word = True

    # Recherche d'un mot dans l'arbre
    def search(self, word):
        node = self.root
        for char in word:
            # Si le caractere du mot nest pas dans le noeud, le mot nexiste pas
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    # Suppression d'un mot
    def delete(self, word):
        def _delete_helper(node, word, depth):
            if depth == len(word):
                # Si la profondeur est maximale, on verifie que le mot est bien "terminé" puis on renvoie un true
                if node.is_end_of_word:
                    node.is_end_of_word = False
                    return len(node.children) == 0
                return False

            char = word[depth]
            if char not in node.children:
                # Si on ne trouve pas le bon caractere a sa place "sensée", on renvoie unFalse
                return False

            should_delete_node = _delete_helper(node.children[char], word, depth + 1)
            if should_delete_node:
                # Le thread remonte la pile de méthodes et vien supprimer les noeuds un par un
                del node.children[char]
                return len(node.children) == 0
            return False

        _delete_helper(self.root, word, 0)
