# eX3 Access - Email Thread

## Email 1

**From:** Tore H. Larsen <torel@simula.no>
**To:** andreasklaeboe@gmail.com
**Date:** 22. mai 2026 kl. 11:33

Hi Andreas,

Welcome to our small but powerful and very heterogeneous cluster!

You should have received a Signal IM or SMS by now with a temporary password. If you have not, please contact me or me on Signal.org APP. Your login is `andreasklaeboe`. Please change the password at first login!

Note that the use of ksripon's username below is just an example. You should replace it with your own in the examples below.

For more information, please refer to https://www.ex3.simula.no/ and http://wiki.ex3.simula.no/doku.php

If you are a Simula employee, I recommend using Forticlient VPN: https://simulink.simula.no/knowledgebase/articles/44/en Clients for Windows, Mac, and Linux can be found here: https://www.fortinet.com/support/product-downloads#vpn You access it with your regular Active directory account. Forticlient mobile VPN clients can be found on Google Play and Apple Appstore.

External users can use tunneling to the login node. Below is an alias I use to connect, or if you prefer, you can set up an ssh config for it.

If you have other software you would like to see installed as modules, email me about it and point me to the software. You can put it in your account under ~/Download. I won't promise I do it swiftly, but I will get to it in time if it is useful for all of us.

Please inform me what resources you would most likely use. There are some restrictions to usage, and in order to get access to some of these resources, you need to ask for it. E.g. DGX-2, Graphcore IPUPOD64, etc.

Lastly, please do not "hog" login nodes too much. If you run things on the login node, limit the threads to 8.

--From the eX³ team!

### Example login for external users using tunneling:

```
[torel@srl-torel01 ~]$ ssh -YAC2 ksripon@dnat.simula.no -p 60441
ksripon@dnat.simula.no's password: *************
```

and you should be login to srl-login1 node.

FortiClient VPN client installation is described in this Simulink article: https://simulink.simula.no/knowledgebase/articles/44/en

With it you can login directly to the cluster.

```
torel@srl-torel01:~$ ssh -Y ksripon@srl-login1.ex3.simula.no
/usr/bin/xauth:  file /home/ksripon/.Xauthority does not exist
You are on an x86_64 node (Epyc or Xeon)

ksripon@srl-login1:~$ module list
Currently Loaded Modulefiles:
 1) slurm/18.08.8(default)   2) ex3-modules   3) google/gdrive/2.1.0  

ksripon@srl-login1:~$ module avail
ksripon@srl-login1:~$ exit
```

If you want to develop on an Arm node (aarch64), do:

```
ksripon@srl-login1:~$ srun -p armq -N 1 -n 32 --mem-per-cpu=0 --pty /bin/bash --login
You are on an Aarch64 node

ksripon@n006:~$ uname -ar
Linux n006 4.15.0-72-generic #81-Ubuntu Tue Nov 26 12:21:09 UTC 2019 aarch64 aarch64 aarch64 GNU/Linux

ksripon@n006:~$ module avail
ksripon@n006:~$ exit
```

**Note!** Alternatively, you can use huaq to access high-end Huawei nodes with DP Kunpeng920-6428 processors (128 core per node) and a Nvidia A40 GPU.

To test and develop on the Nvidia DGX-2, do:

```
ksripon@srl-login1:~$  srun -p dgx2q -N 1 -n 8 --gres=gpu:1 --pty /bin/bash --login
You are on an x86_64 node (Epyc or Xeon)

ksripon@g001:~$ module load cuda12.2/toolkit/12.2.2
ksripon@g001:~$ nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Tue_Aug_15_22:02:13_PDT_2023
Cuda compilation tools, release 12.2, V12.2.140
Build cuda_12.2.r12.2/compiler.33191640_0
ksripon@g001:~$ exit
```

**NOTE!** Running interactively may lock up a GPU if you are logged out or forget. When you want to run, please submit jobs using sbatch <script.sbatch> a command where script.sbatch is your job script. Queues (Slurm partitions) currently available can be seen with sinfo. If you need inspiration for e.g. sbatch scripts for DGX-2 send me an email. You can also contact others in Xing's HPC team and they can assist.

To develop and test the Graphcore IPU system, use:

```
ksripon@srl-login1:~$ srun -p ipuq -N 1 -n 4 --pty /bin/bash --login
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

You are on an x86_64 node (Epyc or Xeon)

ksripon@ipu-pod64-server1:~$ exit
```

Let me know if you have any issues logging in.

Please take a minute to look at the end of your .bashrc script. You'll be able to adapt it to your needs.

Kind Regards / Mvh,
**Tore H. Larsen**
Chief Research Engineer HPC
Email: torel@simula.no
Mobile: +47 918 33 670

Simula Research Laboratory - HPC department
Kristian Augusts gate 23, 0164 Oslo, Norway

---

## Email 2

**From:** Tore H. Larsen <torel@simula.no>
**To:** andreasklaeboe@gmail.com
**Date:** 22. mai 2026 kl. 11:34

Hi Andreas,

Can you install the signal.org app or Slack such that I can securely send you the initial password for eX3? I prefer sending passwords over the Signal APP.

Don't hesitate to contact me at +4791833670 on Signal, and I will send you the temporary password.

Lastly, please ensure you keep personal accounts private from others. Please adhere to the policy found here: https://www.sigma2.no/password-policies

**Ref:**

- https://signal.org/
- https://play.google.com/store/apps/details?id=org.thoughtcrime.securesms&hl=en&gl=US
- https://apps.apple.com/us/app/signal-private-messenger/id874139669

Kind Regards / Mvh,
**Tore H. Larsen**
Chief Research Engineer HPC
Email: torel@simula.no
Mobile: +47 918 33 670

Simula Research Laboratory - HPC department
Kristian Augusts gate 23, 0164 Oslo, Norway

---

## Email 3

**From:** Tore H. Larsen <torel@simula.no>
**To:** andreasklaeboe@gmail.com, andrklae@uio.no
**Date:** 22. mai 2026 kl. 11:37

Please review the attached presentation.

Kind Regards / Mvh,
**Tore H. Larsen**
Chief Research Engineer HPC
Email: torel@simula.no
Mobile: +47 918 33 670

Simula Research Laboratory - HPC department
Kristian Augusts gate 23, 0164 Oslo, Norway

**Attachment:** 2022-11-21-Tools-meetup-guide_to_ex3_for_beginners.pdf (12540K)
