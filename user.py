class User:
  def __init__(self, username, is_authorized, is_admin, has_sudo):
    self.username = username
    self.is_authorized = is_authorized
    self.is_admin = is_admin
    self.has_sudo = has_sudo
