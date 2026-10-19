class PrintJobNode:
    def __init__(self, job_id, student_name, pages):
        self.job_id = job_id
        self.student_name = student_name
        self.pages = pages
        self.next = None


class PrintQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, job_id, student_name, pages):
        node = PrintJobNode(job_id, student_name, pages)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1
        return node

    def dequeue(self):
        if self.front is None:
            return None
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        node.next = None
        self.size -= 1
        return node

    def peek(self):
        return self.front

    def displayQueue(self):
        if self.front is None:
            print("Queue is empty.")
            return
        print("FRONT")
        cur = self.front
        while cur is not None:
            print(f"  {cur.student_name} - {cur.pages} pages (Job {cur.job_id})")
            cur = cur.next
        print("REAR")

    def countJobs(self):
        count, cur = 0, self.front
        while cur is not None:
            count += 1
            cur = cur.next
        return count


def main():
    q = PrintQueue()
    next_id = 1
    while True:
        print("\n1. Add Print Job\n2. Print Next Job\n3. View Next Job\n4. Display Queue\n5. Count Jobs\n6. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            name = input("Student name: ")
            q.enqueue(next_id, name, int(input("Pages: ")))
            next_id += 1
            print("Job added.")
        elif choice == "2":
            j = q.dequeue()
            print(f"{j.student_name} printed successfully." if j else "Queue is empty.")
        elif choice == "3":
            j = q.peek()
            print(f"Next: {j.student_name} - {j.pages} pages" if j else "Queue is empty.")
        elif choice == "4":
            q.displayQueue()
        elif choice == "5":
            print("Jobs:", q.countJobs())
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
