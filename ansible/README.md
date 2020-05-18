
# Configuring a new node

1) Flash Raspbian Buster onto it,
	add wpa_supplicant file into boot drive,
	add ssh file into boot drive

2) Change the passwords of the nodes
	for both `pi` and `root`

3) Change hostname to chlorophyll-NUMBER

4) Configure ssh for `root` (/etc/ssh/sshd_config)

5) Copy ssh keys to `root@hostname`

6) `ansible-playbook -i hosts configure_nodes.yml`
