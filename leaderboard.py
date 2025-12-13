import json
import os
from datetime import datetime

class Leaderboard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        """Memuat data dari file JSON, jika tidak ada buat baru."""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_data(self):
        """Menyimpan data ke file JSON."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"Gagal menyimpan leaderboard: {e}")

    def add_win(self, player_name):
        """
        Menambahkan kemenangan ke pemain. 
        Jika pemain sudah ada, update 'wins'. Jika belum, buat baru.
        """
        player_name = player_name.strip()
        if not player_name: return

        found = False
        for entry in self.data:
            if entry['name'].lower() == player_name.lower():
                entry['wins'] += 1
                entry['last_played'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                found = True
                break
        
        if not found:
            new_entry = {
                "name": player_name,
                "wins": 1,
                "last_played": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.data.append(new_entry)
        
        # Urutkan berdasarkan kemenangan terbanyak
        self.data.sort(key=lambda x: x['wins'], reverse=True)
        self.save_data()

    def get_top_players(self, limit=5):
        """Mengambil top players."""
        return self.data[:limit]