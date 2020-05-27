title: Linux System Administration
date: 2020-05-27
author: Harry
category: development

## Chapter 1: Process Management

Certain shell variables hold process information.

`$$` contains the PID (process id) of the current process.

    echo $$

`$PPID` contains the PID of the **parent process** (the PPID), the process which spawned the current process.

    echo $PPID

Check the current PID, start a new bash process, and then verify that the PPID of that new bash process is the PID of the process from which the current process was spawned.

    echo $$;
    bash;
    echo $PPID;

Processes are created in 2 stages: fork, and exec. The spawning process first creates a copy of itself (the fork), then executes `exec` to replace the fork. `exec` can replace the current process with the command that it executes.

`ps` is a tool to examine processes. It can be invoked with various argument combinations. Two useful argument sets are `aux` and `fax`. 

`aux`, called as `ps aux`, contains `a`, `u`, and `x`, each of which controls some aspect of the output of `ps`. `a` shows processes from all users, `u` displays the owner of the process, and `x` shows 'headless' processes, those not attached to a terminal window. 


