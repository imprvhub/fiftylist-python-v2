# FiftyList Music Automation Platform

Welcome to the repository of [Fifty List - Music Automation Platform](https://fiftylist.vercel.app/) . This project is part of my portfolio showcased at [ivanluna.dev](https://ivanluna.dev) and demonstrates a sophisticated integration of React and Python. For detailed insights, please visit [ivanluna.dev](https://ivanluna.dev).

### Live Demo:
https://fiftylist.vercel.app/

## Key Features

### React Component
- Spotify Integration: Fetches your top 50 tracks from Spotify within a chosen timeframe (1, 6 months, or all-time classics).
- Playlist Creation: Automatically generates a new playlist on your Spotify account with these tracks.
- Recommendation Lists Creation: Based on your top 50 listened songs, our recommendation engine suggests an additional 20 songs to add to your playlists.

### Python Component
- Flask-Powered: Acts as a middleware that interfaces between React and Todoist.
- Task Management: Organizes track details into tasks on Todoist, including artist names, song titles, album names, release dates, and genres.

## About the Project

FiftyList is an exploratory project diving deep into the collaboration of different programming languages and APIs. It is designed to:
- Demonstrate Seamless Communication: Showcases smooth communication between the frontend and backend using API calls.
- Emphasize Language Synergy: Highlights the synergy between React's frontend prowess and Python's backend efficiency.
- Data Presentation Challenge: Ensures that complex data is rendered in a user-friendly format and transmitted effectively between systems.

## Installation and Usage

### For Frontend Installation:
1. Clone the project. ( https://github.com/imprvhub/fiftylist-react )
 ```bash
git clone https://github.com/imprvhub/fiftylist-react.git
```
In your IDE terminal:
1.2 Navigate to the project directory
```bash
cd /your/folder/directory/fiftylist-react
```
3. Run the command `npm install` to install all required dependencies.
4. Replace the environment variables (`REACT_APP_SCOPES`, `REACT_APP_REDIRECT_URI`, `REACT_APP_CLIENT_SECRET`, `REACT_APP_CLIENT_ID`) with your own. You can generate these variables from Spotify Developer Dashboard.
5. Replace the variable defined at the beginning of the code in `App.js`:
   `const redirectUri = 'https://fiftylist.vercel.app/callback';` with -> `const redirectUri = "http://localhost:3000/callback";`
   Update the URLs in the variables of the `exportTodoist` function from `'https://fiftylistbackend.vercel.app/todoist'` to `'http://localhost:5000/todoist'` if your Python backend is using a different 
   port.
6. Run `npm start` from your IDE terminal; this should start the frontend on the designated port. Repeat the process for the backend.

### For Backend Installation:
### Prerequisites:
[**Python 3.11**](https://www.python.org/downloads/release/python-3110/)

1. Clone this project.
 ```bash
git clone https://github.com/imprvhub/fiftylist-python.git
```
In your IDE terminal:
1.2 Navigate to the project directory
```bash
cd /your/folder/directory/fiftylist-python
```
2. Run the command `pip install -r requirements.txt` to install all required dependencies.
3. Replace the variable defined at the beginning of the todoist.py code: `cors = CORS(app, resources={r"/todoist": {"origins": "https://fiftylist-frontend.vercel.app/"}})` with ->  `cors = CORS(app, resources={r"/todoist": {"origins": "http://localhost:3000/"}})` (or the port you designated for your frontend).
4. Run `python3 todoist.py`.
   
IMPORTANT: Open two separate windows in your IDE to run the fullstack locally. Execute the commands to have both projects running simultaneously for them to work seamlessly.

## Contributing

We welcome contributions to the FiftyList project. If you have suggestions or improvements, feel free to contact us at contact@ivanluna.dev.

This project is part of a portfolio at ivanluna.dev - offering a unique fullstack development perspective by fusing React with Python.
