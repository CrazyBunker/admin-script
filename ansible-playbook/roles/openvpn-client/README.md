Role Name
=========
openvpn-client

Role Variables
--------------
````
openvpn_client_dev: tun
openvpn_client_remote: <ip remote>
openvpn_client_remote_port: <port remote>
openvpn_client_remote_protocol: <protocol remote>
openvpn_dst_config: <path to configuration file>
openvpn_client_cert: "{{ lookup('file', 'files/client/client.crt') }}"  #Client certificate path
openvpn_client_key: "{{ lookup('file', 'files/client/client.key') }}"   #Client key path
openvpn_ca: "{{ lookup('file', 'files/client/ca.crt') }}"               #Certificate authority certificate path
openvpn_tls: "{{ lookup('file', 'files/client/tls.key') }}"             #TLS Key Path
````
Key Location: files/clients


Author Information
------------------

Vladislav Plotkin\
e-mail: vlad@krasnodar-it-service.ru\
e-mail: mydisktransport@yandex.ru
