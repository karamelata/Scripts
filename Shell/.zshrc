# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/Users/Dave/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

export EDITOR=emacs

# Add ~/bin to PATH
export PATH=~/bin:$PATH
# Add Racket to PATH
export PATH=/Applications/Racket\ v6.6/bin:$PATH
# Add Python to PATH
#export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
# Add pwd to PATH
export PATH=.:$PATH

alias bp='nano ~/.zshrc'
alias src='source ~/.zshrc'
alias ls='ls -gh'
alias l='ls'
alias lf='find . -maxdepth 1 -type f'
alias ldir='ls -d */'
alias ~='cd ~'
alias o=open
alias oa='open -a'
alias od='open .'
alias c=clear
alias h=history
alias x=exit
alias path='echo -e ${PATH//:/\\n}'
alias now=date
alias zs='zsh_stats'
alias temacs='$EDITOR --no-window-system'
alias oew='$EDITOR'
alias oe=temacs
alias trashit='rm -rf ~/.Trash/'

alias p2='python'
alias p3='python3'
alias mongod='mongod --dbpath /Users/Dave/.mongodb/data'

# Web Shortcuts
alias chrome="open -a \"Google Chrome\""
alias gh="chrome http://github.com/davemachado"
alias email="chrome http://inbox.google.com"
alias djs="python manage.py runserver"

# Scripts
alias mkgo=". mkgo"

# Networking
# Stop after sending count ECHO_REQUEST packets #
alias ping='ping -c 5'
# Do not wait interval 1 second, go fast #
alias fastping='ping -c 100 -s.2'
alias ports='netstat -tulanp'
alias net='nmap -sn 192.168.1.0/24'
alias xip='curl https://myexternalip.com/raw'
# Syntax Highlighting installed from Homebrew
source /usr/local/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
export JAVA_HOME=$(/usr/libexec/java_home)
