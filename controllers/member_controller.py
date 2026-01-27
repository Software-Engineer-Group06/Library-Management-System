from models.member import MemberModel
from views.member_view import MemberView

class MemberController:
    def __init__(self):
        self.model = MemberModel()
        self.view = MemberView()

    def run_register(self):
        data = self.view.get_register_input()
        
        if data:
            # Gọi Model (Tự sinh ID bên trong)
            new_id = self.model.add_member(data)
            
            if new_id:
                # Hiển thị ID vừa tạo
                self.view.display_register_success(new_id)
            else:
                self.view.display_msg("Registration failed. System Error.")

    def run_update(self):
        m_id = self.view.get_member_id_input("Update")
        current = self.model.get_member_details(m_id)
        
        if not current:
            self.view.display_msg("Member ID not found.")
            return

        new_data = self.view.get_update_input(current)
        if new_data:
            if self.model.update_member(m_id, new_data):
                self.view.display_msg("Member updated successfully.")
            else:
                self.view.display_msg("Update failed.")
        else:
            self.view.display_msg("Invalid input.")

    def run_delete(self):
        m_id = self.view.get_member_id_input("Delete")
        if self.model.delete_member(m_id):
            self.view.display_msg("Member deleted successfully.")
        else:
            self.view.display_msg("Delete failed. Member may have active borrowings or ID not found.")