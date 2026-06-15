# ACFA Welcome Board Image Auto Update

This repo creates a self-updating PNG image for the And Chess For All Chess.com sidebar.

## What it does

- Pulls newest members from the Chess.com Public API
- Creates `acfa-welcome-board.png`
- Updates every 6 hours using GitHub Actions
- Lets Chess.com display a dynamic-looking board using only an image

## Setup

1. Create a new GitHub repository.
2. Upload every file from this folder into the repository.
3. Go to the repository's **Actions** tab.
4. Enable workflows if GitHub asks.
5. Run **Update ACFA Welcome Board** manually once.
6. After it finishes, the file `acfa-welcome-board.png` should appear.

## Chess.com Sidebar Image Code

Replace `YOUR-GITHUB-USERNAME` and `YOUR-REPO-NAME`:

```html
<div style="background:#0d0d0d;border:2px solid #ffd700;border-radius:12px;padding:12px;margin-top:15px;margin-bottom:15px;box-shadow:0 0 12px #b8860b;text-align:center;">

  <h2 style="color:#ffd700;margin-top:0;text-shadow:0 0 8px #ffd700;">
    👋 Live Welcome Board
  </h2>

  <img src="https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME/main/acfa-welcome-board.png"
       alt="ACFA Live Welcome Board"
       style="width:100%;border-radius:10px;border:1px solid #ffd700;box-shadow:0 0 10px #ffd700;">

</div>
```

## Notes

GitHub Actions updates the image every 6 hours. Chess.com may cache the image, so changes might not appear instantly.
