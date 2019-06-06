Role Name
=========

Create, remove or lock users

Requirements
------------

    This role requires ansible 1.9 or higher.
    Default password: pass
    For create new password, please run (mkpasswd -m SHA-512), and change key password: $6$xxx...

Role Variables
--------------

    adduser:
      users:
        - name: username
          pubkey: "{{ lookup('file', '~/.ssh/pubkeys/username.pub') }}"
          groups: users
          change: false
        - name: username1
          pubkey: "ssh-rsa AAAAB3NzaC1yc2EAA... username@hostname"
          change: true
    rmuser:
      users:
        - username2
    lock:
      users:
        - username3
    deployuser: true

Default vars in role:

    defgroup: users  
    deployuser: false  

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role:

    - hosts: servers
      become: true
      roles:
         - { role: adduser }

License
-------

BSD

Author Information
------------------

Created by CHIP0K
