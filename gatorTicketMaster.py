import sys
from TicketMaster import TicketMaster


def process_command(ticket_master, command: str) -> str:
    """Process a single command and return the output."""
    # Split command into function name and parameters
    parts = command.strip().split('(')
    if len(parts) != 2 or not parts[1].endswith(')'):
        return "Invalid command format"

    func_name = parts[0].strip()
    params = parts[1][:-1].split(',')
    params = [param.strip() for param in params if param.strip()]

    # Map commands to functions
    try:
        if func_name == "Initialize":
            return ticket_master.initialize(int(params[0]))
        elif func_name == "Available":
            return ticket_master.available()
        elif func_name == "Reserve":
            return ticket_master.reserve(int(params[0]), int(params[1]))
        elif func_name == "Cancel":
            return ticket_master.cancel(int(params[0]), int(params[1]))
        elif func_name == "ExitWaitlist":
            return ticket_master.exit_waitlist(int(params[0]))
        elif func_name == "UpdatePriority":
            return ticket_master.update_priority(int(params[0]), int(params[1]))
        elif func_name == "AddSeats":
            return ticket_master.add_seats(int(params[0]))
        elif func_name == "PrintReservations":
            return ticket_master.print_reservations()
        elif func_name == "ReleaseSeats":
            return ticket_master.release_seats(int(params[0]), int(params[1]))
        elif func_name == "Quit":
            return ticket_master.quit()
        else:
            return f"Unknown command: {func_name}"
    except (ValueError, IndexError) as e:
        return f"Invalid parameters for command {func_name}"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gatorTicketMaster.py <input_file>")
        return

    input_file = sys.argv[1]
    output_file = input_file.rsplit('.', 1)[0] + "_output_file.txt"

    ticket_master = TicketMaster()

    try:
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for line in f_in:
                line = line.strip()
                if not line:
                    continue

                result = process_command(ticket_master, line)
                f_out.write(result + "\n")

                if line.startswith("Quit"):
                    break
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
    except Exception as e:
        print(f"Error processing commands: {str(e)}")


if __name__ == "__main__":
    main()
