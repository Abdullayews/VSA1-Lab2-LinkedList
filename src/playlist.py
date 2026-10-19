class SongNode:
    def __init__(self, song_id, name, artist, duration):
        self.song_id = song_id
        self.name = name
        self.artist = artist
        self.duration = duration
        self.next = None


class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.current = None  # playNextSong ucun

    def addSong(self, song_id, name, artist, duration):
        node = SongNode(song_id, name, artist, duration)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1
        return node

    def deleteSong(self, song_id):
        prev, cur = None, self.head
        while cur is not None and cur.song_id != song_id:
            prev, cur = cur, cur.next
        if cur is None:
            return False
        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next
        if cur is self.tail:
            self.tail = prev
        if cur is self.current:
            self.current = prev
        self.size -= 1
        return True

    def searchSong(self, song_id):
        cur = self.head
        while cur is not None:
            if cur.song_id == song_id:
                return cur
            cur = cur.next
        return None

    def displayPlaylist(self):
        if self.head is None:
            print("Playlist is empty.")
            return
        cur = self.head
        while cur is not None:
            print(f"[{cur.song_id}] {cur.name} - {cur.artist} ({cur.duration}) -> ", end="")
            cur = cur.next
        print("None")

    def countSongs(self):
        count, cur = 0, self.head
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def playNextSong(self):
        if self.head is None:
            print("Playlist is empty.")
            return None
        self.current = self.head if self.current is None or self.current.next is None else self.current.next
        s = self.current
        print(f"Now playing: {s.name} - {s.artist} ({s.duration})")
        return s


def main():
    pl = Playlist()
    while True:
        print("\n1. Add Song\n2. Delete Song\n3. Search Song\n4. Display Playlist\n5. Play Next Song\n6. Count Songs\n7. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            sid = int(input("ID: "))
            if pl.searchSong(sid):
                print("Song with this ID already exists.")
                continue
            pl.addSong(sid, input("Name: "), input("Artist: "), input("Duration: "))
            print("Song added successfully.")
        elif choice == "2":
            print("Song deleted." if pl.deleteSong(int(input("ID: "))) else "Song not found.")
        elif choice == "3":
            s = pl.searchSong(int(input("ID: ")))
            print(f"Found: {s.name} - {s.artist} ({s.duration})" if s else "Song not found.")
        elif choice == "4":
            pl.displayPlaylist()
        elif choice == "5":
            pl.playNextSong()
        elif choice == "6":
            print("Songs:", pl.countSongs())
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
