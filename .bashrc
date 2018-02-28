#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias ssh="TERM=rxvt ssh"
alias please='sudo'
#alias pmi='sudo pacman -Syu --config /etc/pacman-zfs.conf --ignore linux'
#alias pui='pacaur -Syu --ignore linux,oracle-sqldeveloper'
export WINEPREFIX=~/win32
export WINEARCH=win32
alias pacm='sudo pacman -Syu --config /etc/pacman-zfs.conf'
alias paca='pacaur -Syu'
alias q='LC_ALL="ru_RU.CP1251" WINEDEBUG=odbc'
PS1='[\u@\h \W]\$' 
alias tm="tmux new-session -A -s $USER"
