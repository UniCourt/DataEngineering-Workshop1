# Introduction to Git.
<br />

### Setting up github:

``` 
Make a repository in GitHub

     Go to GitHub.com and login.
     Click the green “New Repository” button
             Repository name: myrepo
             Public
             Check Initialize this repository with a README
             Click the green “Create repository” button
     Copy the HTTPS clone URL to your clipboard via the green “Clone or Download” button.
Clone the repository to your computer

     git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
    
Make a local change, commit, and push

     git add <file path>	//here the file path is which file you modified ready the file for commit
     git commit -m "A commit from my local computer"	      //here you commit the changes
     git push origin <brachname> 	//here you push the changes to your remote repository and brach name is in which brach you pushing this
```
<br />

### General git flow:
         ![git flow](gitflow.png)

```
Basic commands of git:

git init
the command git init is used to create an empty Git repository.

git add
 Add command is used after checking the status of the files, to add t	hose files to the staging area.
 Before running the commit command, "git add" is used to add any new or modified files.

git commit
 The commit command makes sure that the changes are saved to the local repository.
 The command "git commit –m <message>" allows you to describe everyone and help them understand what has happened.

git status
 The git status command tells the current state of the repository.
 The command provides the current working branch. If the files are in the staging area, but not committed, it will be shown by the git status. 
 Also, if there are no changes, it will show the message no changes to commit, working directory clean.
 
git config
The git config command is used initially to configure the user.name and user.email. This specifies what email id and username will be used from a local repository.
```

        