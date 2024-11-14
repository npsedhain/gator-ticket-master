import time
from RedBlackTree import RedBlackTree
from BinaryMinHeap import BinaryMinHeap

class TicketMaster:
    def __init__(self):
        self.reserved_seats = RedBlackTree()  # Maps user_id to seat_id
        self.waitlist = BinaryMinHeap()  # Priority queue for waiting users
        self.available_seats = BinaryMinHeap()  # Heap for available seat numbers
        self.seat_to_user = {}  # Quick lookup for seat to user mapping
        self.max_seat_number = 0  # Keep track of highest seat number

    def initialize(self, seat_count: int) -> str:
        """Initialize the events with specified number of seats."""
        try:
            seat_count = int(seat_count)
            if seat_count <= 0:
                return "Invalid input. Please provide a valid number of seats."

            # Reset all data structures
            self.reserved_seats = RedBlackTree()
            self.waitlist = BinaryMinHeap()
            self.available_seats = BinaryMinHeap()
            self.seat_to_user = {}

            # Add all seats to available seats heap
            for i in range(1, seat_count + 1):
                # Using negative priority for min heap behavior
                self.available_seats.insert(-i, i, time.time())

            self.max_seat_number = seat_count
            return f"{seat_count} Seats are made available for reservation"
        except ValueError:
            return "Invalid input. Please provide a valid number of seats."

    def available(self) -> str:
        """Print the number of available seats and waitlist length."""
        available_count = self.available_seats.size()
        waitlist_count = self.waitlist.size()
        return f"Total Seats Available : {available_count}, Waitlist : {waitlist_count}"

    def reserve(self, user_id: int, user_priority: int) -> str:
        """Allow a user to reserve a seat or join the waitlist."""
        # If seats are available, assign the lowest numbered seat
        if not self.available_seats.is_empty():
            # Will get lowest number due to negative priority
            seat_node = self.available_seats.extract_max()
            seat_id = seat_node.user_id  # We stored seat_id in user_id field

            # Update data structures
            self.reserved_seats.insert(user_id, seat_id)
            self.seat_to_user[seat_id] = user_id

            return f"User {user_id} reserved seat {seat_id}"
        else:
            # Add user to waitlist
            self.waitlist.insert(user_priority, user_id, time.time())
            return f"User {user_id} is added to the waiting list"

    def cancel(self, seat_id: int, user_id: int) -> str:
        """Cancel a reservation and reassign seat if waitlist is not empty."""
        # Verify the seat belongs to the user
        if seat_id not in self.seat_to_user:
            return f"User {user_id} has no reservation to cancel"

        if self.seat_to_user[seat_id] != user_id:
            return f"User {user_id} has no reservation for seat {seat_id} to cancel"

        # Remove the reservation
        node = self.reserved_seats.search(user_id)
        if node:
            self.reserved_seats.delete(node)
            del self.seat_to_user[seat_id]

            # If waitlist is not empty, assign seat to next user
            if not self.waitlist.is_empty():
                next_user = self.waitlist.extract_max()
                self.reserved_seats.insert(next_user.user_id, seat_id)
                self.seat_to_user[seat_id] = next_user.user_id
                return f"User {user_id} canceled their reservation\nUser {next_user.user_id} reserved seat {seat_id}"
            else:
                # Add seat back to available seats
                self.available_seats.insert(-seat_id, seat_id, time.time())
                return f"User {user_id} canceled their reservation"

        return f"User {user_id} has no reservation to cancel"

    def exit_waitlist(self, user_id: int) -> str:
        """Remove a user from the waitlist."""
        if self.waitlist.contains(user_id):
            self.waitlist.remove(user_id)
            return f"User {user_id} is removed from the waiting list"
        return f"User {user_id} is not in waitlist"

    def update_priority(self, user_id: int, new_priority: int) -> str:
        """Update the priority of a user in the waitlist."""
        if self.waitlist.contains(user_id):
            self.waitlist.update_priority(user_id, new_priority)
            return f"User {user_id} priority has been updated to {new_priority}"
        return f"User {user_id} priority is not updated"

    def add_seats(self, count: int) -> str:
        """Add new seats to the venue."""
        try:
            count = int(count)
            if count <= 0:
                return "Invalid input. Please provide a valid number of seats."

            start_seat = self.max_seat_number + 1
            end_seat = start_seat + count
            result = [f"Additional {count} Seats are made available for reservation"]

            # Add new seats and assign to waitlist users first
            for seat_id in range(start_seat, end_seat):
                self.max_seat_number = seat_id

                if not self.waitlist.is_empty():
                    next_user = self.waitlist.extract_max()
                    self.reserved_seats.insert(next_user.user_id, seat_id)
                    self.seat_to_user[seat_id] = next_user.user_id
                    result.append(
                        f"User {next_user.user_id} reserved seat {seat_id}")
                else:
                    self.available_seats.insert(-seat_id, seat_id, time.time())

            return "\n".join(result)
        except ValueError:
            return "Invalid input. Please provide a valid number of seats."

    def print_reservations(self) -> str:
        """Print all current reservations ordered by seat number."""
        reservations = self.reserved_seats.inorder_traverse()
        return "\n".join([f"Seat {seat}, User {user}" for seat, user in reservations])

    def release_seats(self, user_id1: int, user_id2: int) -> str:
        """Release all seats in the given user ID range."""
        try:
            if user_id1 > user_id2:
                return "Invalid input. Please provide a valid range of users."

            # Collect all seats to be released
            seats_to_release = []
            users_to_remove = []

            # Find all reservations in the range
            for seat_id, current_user_id in self.seat_to_user.items():
                if user_id1 <= current_user_id <= user_id2:
                    seats_to_release.append(seat_id)
                    users_to_remove.append(current_user_id)

            # Remove users from waitlist in the range
            for user_id in range(user_id1, user_id2 + 1):
                if self.waitlist.contains(user_id):
                    self.waitlist.remove(user_id)

            result = ["Reservations of the Users in the range " + f"[{user_id1}, {user_id2}] are released"]

            # Release seats and reassign if possible
            for seat_id, user_id in zip(seats_to_release, users_to_remove):
                node = self.reserved_seats.search(user_id)
                if node:
                    self.reserved_seats.delete(node)
                    del self.seat_to_user[seat_id]

                    # If waitlist not empty, assign seat to next user
                    if not self.waitlist.is_empty():
                        next_user = self.waitlist.extract_max()
                        self.reserved_seats.insert(next_user.user_id, seat_id)
                        self.seat_to_user[seat_id] = next_user.user_id
                        result.append(f"User {next_user.user_id} reserved seat {seat_id}")
                    else:
                        self.available_seats.insert(-seat_id,seat_id, time.time())

            return "\n".join(result)
        except ValueError:
            return "Invalid input. Please provide a valid range of users."

    def quit(self) -> str:
        """Terminate the program."""
        return "Program Terminated!!"
