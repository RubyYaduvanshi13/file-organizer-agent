# Create some test files for the agent to organize
cd agent_workspace 2>/dev/null || mkdir agent_workspace && cd agent_workspace

# Create various file types
echo "Project report" > report.pdf
echo "Vacation photo" > photo.jpg
echo "Meeting notes" > notes.txt
echo "Budget 2024" > budget.xlsx
echo "Python script" > script.py
echo "Music song" > song.mp3
echo "Video recording" > video.mp4
echo "Random file" > random.xyz

# Go back to main folder
cd ..

echo "✅ Created 8 test files in agent_workspace/"
echo ""
echo "📁 Files ready to organize:"
ls -la agent_workspace/