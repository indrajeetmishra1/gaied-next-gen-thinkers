import uuid
import email
from email.policy import default
import os
import imaplib

class TicketSystem:
    def __init__(self):
        self.tickets = {}  # Maps original message IDs to ticket numbers
    
    def process_eml(self, eml_path):
        """Process an .eml file and return (ticket_number, is_existing)"""
        msg = self._parse_eml(eml_path)
        return self._process_message(msg)

    def process_server_email(self, raw_email_bytes):
        """Process email from server and return (ticket_number, is_existing)"""
        msg = email.message_from_bytes(raw_email_bytes, policy=default)
        return self._process_message(msg)

    def _process_message(self, msg):
        """Common processing logic returning (ticket, exists) tuple"""
        message_id = msg['Message-ID']
        references = msg['References'] or ''
        in_reply_to = msg['In-Reply-To'] or ''

        # Find original message in thread
        original_id = self._find_original_id(
            references.split() + in_reply_to.split()
        )

        # Check for existing ticket in thread
        if original_id and original_id in self.tickets:
            return (self.tickets[original_id], True)

        # Check if current message already has a ticket
        if message_id in self.tickets:
            return (self.tickets[message_id], True)

        # Create new ticket
        new_ticket = self._generate_ticket_number()
        self.tickets[message_id] = new_ticket
        return (new_ticket, False)

    def _parse_eml(self, eml_path):
        """Parse .eml file and return Message object"""
        with open(eml_path, 'r', encoding='utf-8') as f:
            return email.message_from_file(f, policy=default)

    def _find_original_id(self, references):
        """Find the original message ID from reference headers"""
        return references[0] if references else None

    def _generate_ticket_number(self):
        """Generate random ticket number"""
        return str(uuid.uuid4())

# # Example usage
# if __name__ == "__main__":
#     ts = TicketSystem()
    
#     # Process directory of .eml files
#     eml_dir = 'emails'
#     for filename in sorted(os.listdir(eml_dir)):
#         if filename.endswith('.eml'):
#             eml_path = os.path.join(eml_dir, filename)
#             ticket = ts.process_eml(eml_path)
#             print(f"{filename}: Ticket {ticket}")