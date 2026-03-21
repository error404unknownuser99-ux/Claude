# 🧪 Testing URLs — GitHub Proxy Server

Base URL: `https://git-hub-remote-five.vercel.app`

---

## 👤 User Tests

```
https://git-hub-remote-five.vercel.app/github?action=get_user&username=torvalds
https://git-hub-remote-five.vercel.app/github?action=get_user&username=octocat
https://git-hub-remote-five.vercel.app/github?action=get_followers&username=torvalds
https://git-hub-remote-five.vercel.app/github?action=get_following&username=octocat
```

---

## 📁 Repository Tests

```
https://git-hub-remote-five.vercel.app/github?action=get_repo&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=get_repo&owner=facebook&repo=react
https://git-hub-remote-five.vercel.app/github?action=list_repos&owner=google&type=public
https://git-hub-remote-five.vercel.app/github?action=get_languages&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=get_topics&owner=microsoft&repo=vscode
```

---

## 📄 File & Content Tests

```
https://git-hub-remote-five.vercel.app/github?action=get_readme&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=list_files&owner=facebook&repo=react&path=packages
https://git-hub-remote-five.vercel.app/github?action=get_file&owner=torvalds&repo=linux&path=README
```

---

## 🌿 Branch Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_branches&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=get_branch&owner=facebook&repo=react&branch=main
```

---

## 🐛 Issue Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_issues&owner=facebook&repo=react&state=open
https://git-hub-remote-five.vercel.app/github?action=list_issues&owner=microsoft&repo=vscode&state=closed&labels=bug
https://git-hub-remote-five.vercel.app/github?action=get_issue&owner=facebook&repo=react&issue_number=1
```

---

## ✅ Commit Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_commits&owner=microsoft&repo=vscode&per_page=5
https://git-hub-remote-five.vercel.app/github?action=compare_commits&owner=facebook&repo=react&base=main&head=0.3-stable
```

---

## 🔀 Pull Request Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_prs&owner=microsoft&repo=vscode&state=open
https://git-hub-remote-five.vercel.app/github?action=get_pr&owner=facebook&repo=react&pr_number=1
```

---

## ⚙️ GitHub Actions Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_workflows&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=list_workflow_runs&owner=microsoft&repo=vscode&workflow_id=ci.yml
```

---

## 🔍 Search Tests

```
https://git-hub-remote-five.vercel.app/github?action=search_repos&q=nodejs&sort=stars
https://git-hub-remote-five.vercel.app/github?action=search_repos&q=react+language:javascript&sort=stars
https://git-hub-remote-five.vercel.app/github?action=search_users&q=location:india+followers:>5000
https://git-hub-remote-five.vercel.app/github?action=search_issues&q=memory+leak+is:open+repo:nodejs/node
```

---

## 🚀 Release Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_releases&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=get_latest_release&owner=microsoft&repo=vscode
```

---

## 📊 Stats Tests

```
https://git-hub-remote-five.vercel.app/github?action=get_contributors&owner=microsoft&repo=vscode
https://git-hub-remote-five.vercel.app/github?action=get_commit_activity&owner=facebook&repo=react
https://git-hub-remote-five.vercel.app/github?action=get_participation&owner=microsoft&repo=vscode
```

---

## 🏢 Organization Tests

```
https://git-hub-remote-five.vercel.app/github?action=get_org&org=microsoft
https://git-hub-remote-five.vercel.app/github?action=list_org_repos&org=google&type=public
https://git-hub-remote-five.vercel.app/github?action=list_org_members&org=microsoft
```

---

## 📝 Gist Tests

```
https://git-hub-remote-five.vercel.app/github?action=list_gists&username=octocat
https://git-hub-remote-five.vercel.app/github?action=get_gist&gist_id=6cad326836d38bd3a7ae
```

---

## 📋 Meta Tests

```
https://git-hub-remote-five.vercel.app/github?action=rate_limit
https://git-hub-remote-five.vercel.app/github?action=help
```

---

## 🧪 External Testing Domains

```
https://jsonplaceholder.typicode.com/posts/1
https://jsonplaceholder.typicode.com/users/1
https://jsonplaceholder.typicode.com/todos/1
```
