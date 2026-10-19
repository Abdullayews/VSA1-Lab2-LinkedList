from datetime import datetime


class ActionNode:
    def __init__(self, action_id, name):
        self.action_id = action_id
        self.name = name
        self.time = datetime.now().strftime("%H:%M:%S")
        self.next = None


class UndoStack:
    def __init__(self):
        self.top = None
        self.size = 0

    def pushAction(self, action_id, name):
        node = ActionNode(action_id, name)
        node.next = self.top
        self.top = node
        self.size += 1
        return node

    def undoAction(self):
        if self.top is None:
            return None
        node = self.top
        self.top = node.next
        node.next = None
        self.size -= 1
        return node

    def currentAction(self):
        return self.top

    def displayHistory(self):
        if self.top is None:
            print("History is empty.")
            return
        print("TOP")
        cur = self.top
        while cur is not None:
            print(f"  [{cur.action_id}] {cur.name} ({cur.time})")
            cur = cur.next

    def countActions(self):
        count, cur = 0, self.top
        while cur is not None:
            count += 1
            cur = cur.next
        return count


def main():
    st = UndoStack()
    next_id = 1
    while True:
        print("\n1. Perform Action\n2. Undo Action\n3. View Current Action\n4. Display Full History\n5. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            st.pushAction(next_id, input("Action name: "))
            next_id += 1
            print("Action performed.")
        elif choice == "2":
            n = st.undoAction()
            print(f"Undo: {n.name}" if n else "Nothing to undo.")
        elif choice == "3":
            n = st.currentAction()
            print(f"Current: {n.name} ({n.time})" if n else "No actions.")
        elif choice == "4":
            st.displayHistory()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
