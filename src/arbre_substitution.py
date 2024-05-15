class Noeud:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class TrieSubstitution:
    def __init__(self, errors: int = 0):
        self.root = Noeud()
        self.errors = errors

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

    @staticmethod
    def remove_str_index(text, index=0, replacement=""):
        return f"{text[:index]}{replacement}{text[index+1:]}"

    def search(self, word):
        return self._search_helper(word, errors=0)

    # Recherche d'un mot dans l'arbre
    def _search_helper(self, word, errors=0):
        node = self.root
        for index, char in enumerate(word):
            if char not in node.children:
                errors += 1
                # print("word: ", word, char, index)
                if errors > self.errors:
                    return False
                # print(f"on loop la parce que la lettre {char} est pas bonne")
                for i in node.children:
                    return self._search_helper(
                        self.remove_str_index(word, index, i), errors
                    )

            if node.children.get(char):
                node = node.children[char]
            else:
                return False
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