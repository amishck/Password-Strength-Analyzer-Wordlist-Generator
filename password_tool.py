#!/usr/bin/env python3
"""
Password Strength Analyzer with Custom Wordlist Generator
A comprehensive tool for analyzing password strength and generating custom wordlists
"""
# Developed By Amishck
import argparse
import re
import math
import itertools
import string
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading

class PasswordAnalyzer:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "password123", "admin", "qwerty",
            "letmein", "welcome", "monkey", "1234567890", "abc123"
        ]
        
        self.keyboard_patterns = [
            "qwerty", "asdf", "zxcv", "123456", "qwertyuiop",
            "asdfghjkl", "zxcvbnm", "1qaz2wsx", "qazwsx"
        ]
    
    def calculate_entropy(self, password):
        """Calculate password entropy"""
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            charset_size += 32
        
        if charset_size == 0:
            return 0
        
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def check_common_patterns(self, password):
        """Check for common password patterns"""
        issues = []
        password_lower = password.lower()
        
        # Check common passwords
        if password_lower in [p.lower() for p in self.common_passwords]:
            issues.append("Uses common password")
        
        # Check keyboard patterns
        for pattern in self.keyboard_patterns:
            if pattern in password_lower or pattern[::-1] in password_lower:
                issues.append(f"Contains keyboard pattern: {pattern}")
        
        # Check repetitive characters
        if re.search(r'(.)\1{2,}', password):
            issues.append("Contains repetitive characters")
        
        # Check sequential numbers
        if re.search(r'(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210)', password):
            issues.append("Contains sequential numbers")
        
        # Check common substitutions
        substitutions = {'@': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's', '7': 't'}
        desubstituted = password_lower
        for num, letter in substitutions.items():
            desubstituted = desubstituted.replace(num, letter)
        
        if desubstituted in [p.lower() for p in self.common_passwords]:
            issues.append("Uses common password with simple substitutions")
        
        return issues
    
    def analyze_password(self, password):
        """Comprehensive password analysis"""
        if not password:
            return {"error": "Password cannot be empty"}
        
        analysis = {
            "password": password,
            "length": len(password),
            "entropy": self.calculate_entropy(password),
            "character_sets": [],
            "patterns": self.check_common_patterns(password),
            "strength_score": 0,
            "strength_label": "",
            "recommendations": []
        }
        
        # Character set analysis
        if re.search(r'[a-z]', password):
            analysis["character_sets"].append("lowercase")
        if re.search(r'[A-Z]', password):
            analysis["character_sets"].append("uppercase")
        if re.search(r'[0-9]', password):
            analysis["character_sets"].append("digits")
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            analysis["character_sets"].append("special")
        
        # Calculate strength score
        score = 0
        
        # Length scoring
        if analysis["length"] >= 12:
            score += 25
        elif analysis["length"] >= 8:
            score += 15
        elif analysis["length"] >= 6:
            score += 5
        
        # Character diversity scoring
        score += len(analysis["character_sets"]) * 15
        
        # Entropy scoring
        if analysis["entropy"] >= 60:
            score += 25
        elif analysis["entropy"] >= 40:
            score += 15
        elif analysis["entropy"] >= 25:
            score += 5
        
        # Penalty for patterns
        score -= len(analysis["patterns"]) * 10
        
        analysis["strength_score"] = max(0, min(100, score))
        
        # Strength labels
        if analysis["strength_score"] >= 80:
            analysis["strength_label"] = "Very Strong"
        elif analysis["strength_score"] >= 60:
            analysis["strength_label"] = "Strong"
        elif analysis["strength_score"] >= 40:
            analysis["strength_label"] = "Moderate"
        elif analysis["strength_score"] >= 20:
            analysis["strength_label"] = "Weak"
        else:
            analysis["strength_label"] = "Very Weak"
        
        # Recommendations
        if analysis["length"] < 8:
            analysis["recommendations"].append("Increase length to at least 8 characters")
        if analysis["length"] < 12:
            analysis["recommendations"].append("Consider using 12+ characters for better security")
        if "lowercase" not in analysis["character_sets"]:
            analysis["recommendations"].append("Include lowercase letters")
        if "uppercase" not in analysis["character_sets"]:
            analysis["recommendations"].append("Include uppercase letters")
        if "digits" not in analysis["character_sets"]:
            analysis["recommendations"].append("Include numbers")
        if "special" not in analysis["character_sets"]:
            analysis["recommendations"].append("Include special characters")
        if analysis["patterns"]:
            analysis["recommendations"].append("Avoid common patterns and dictionary words")
        
        return analysis

class WordlistGenerator:
    def __init__(self):
        self.leetspeak_map = {
            'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
            's': ['5', '$'], 't': ['7'], 'l': ['1'], 'g': ['9'],
            'b': ['8'], 'z': ['2']
        }
    
    def generate_years(self, start_year=1950, end_year=None):
        """Generate list of years"""
        if end_year is None:
            end_year = datetime.now().year + 5
        return [str(year) for year in range(start_year, end_year + 1)]
    
    def generate_dates(self, birth_year=None):
        """Generate common date formats"""
        dates = []
        current_year = datetime.now().year
        
        # Common date formats
        for year in range(1950, current_year + 1):
            dates.extend([
                str(year), str(year)[2:],  # 1990, 90
            ])
        
        # Month/day combinations
        for month in range(1, 13):
            for day in range(1, 32):
                dates.extend([
                    f"{month:02d}{day:02d}",  # 0101
                    f"{day:02d}{month:02d}",  # 0101
                    f"{month}{day:02d}",      # 101
                    f"{day}{month:02d}",      # 101
                ])
        
        if birth_year:
            # Special focus on birth year
            dates.extend([
                str(birth_year), str(birth_year)[2:],
                f"19{str(birth_year)[2:]}", f"20{str(birth_year)[2:]}"
            ])
        
        return list(set(dates))  # Remove duplicates
    
    def apply_leetspeak(self, word):
        """Apply leetspeak transformations"""
        variants = [word]
        word_lower = word.lower()
        
        # Single character substitutions
        for char, replacements in self.leetspeak_map.items():
            for replacement in replacements:
                if char in word_lower:
                    variants.append(word_lower.replace(char, replacement))
        
        # Multiple character substitutions
        leet_word = word_lower
        for char, replacements in self.leetspeak_map.items():
            if char in leet_word:
                leet_word = leet_word.replace(char, replacements[0])
        variants.append(leet_word)
        
        return list(set(variants))
    
    def generate_case_variations(self, word):
        """Generate case variations"""
        return [
            word.lower(),
            word.upper(),
            word.capitalize(),
            word.title()
        ]
    
    def generate_custom_wordlist(self, user_inputs):
        """Generate custom wordlist based on user inputs"""
        wordlist = set()
        
        # Base words from user inputs
        base_words = []
        for key, value in user_inputs.items():
            if value and isinstance(value, str):
                base_words.extend(value.split())
            elif value and isinstance(value, list):
                base_words.extend(value)
        
        # Clean and prepare base words
        cleaned_words = []
        for word in base_words:
            cleaned = re.sub(r'[^\w]', '', str(word))
            if cleaned and len(cleaned) > 1:
                cleaned_words.append(cleaned)
        
        # Generate variations for each base word
        for word in cleaned_words:
            # Original word variations
            wordlist.update(self.generate_case_variations(word))
            
            # Leetspeak variations
            wordlist.update(self.apply_leetspeak(word))
            
            # Reversed
            wordlist.add(word[::-1])
        
        # Combinations with numbers and dates
        years = self.generate_years(1950, 2030)
        common_numbers = ['1', '12', '123', '1234', '12345', '123456',
                         '01', '02', '03', '21', '69', '88', '99']
        
        # Add year/number combinations
        for word in list(wordlist.copy()):
            if len(word) > 2:  # Only for substantial words
                # Append years
                for year in years[:20]:  # Limit to recent years
                    wordlist.add(f"{word}{year}")
                    wordlist.add(f"{word}{year[2:]}")
                
                # Append common numbers
                for num in common_numbers:
                    wordlist.add(f"{word}{num}")
                    wordlist.add(f"{num}{word}")
        
        # Add common passwords with user info
        common_patterns = ['password', 'admin', 'user', 'login', 'welcome']
        for pattern in common_patterns:
            for word in cleaned_words[:5]:  # Limit combinations
                wordlist.add(f"{pattern}{word}")
                wordlist.add(f"{word}{pattern}")
        
        # Remove empty strings and sort
        wordlist = {w for w in wordlist if w and len(w) >= 3}
        return sorted(list(wordlist))
    
    def export_wordlist(self, wordlist, filename):
        """Export wordlist to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in wordlist:
                    f.write(f"{word}\n")
            return True
        except Exception as e:
            print(f"Error exporting wordlist: {e}")
            return False

class PasswordToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer & Wordlist Generator [Amish Ck]")
        self.root.geometry("800x600")
        
        self.analyzer = PasswordAnalyzer()
        self.generator = WordlistGenerator()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Password Analysis Tab
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Password Analysis")
        
        # Password input
        ttk.Label(analysis_frame, text="Password to Analyze:").pack(pady=5)
        self.password_entry = ttk.Entry(analysis_frame, show="*", width=50)
        self.password_entry.pack(pady=5)
        
        ttk.Button(analysis_frame, text="Analyze Password", 
                  command=self.analyze_password).pack(pady=5)
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(analysis_frame, text="Show Password", 
                       variable=self.show_password_var,
                       command=self.toggle_password_visibility).pack(pady=5)
        
        # Results display
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, height=20, width=80)
        self.analysis_text.pack(fill='both', expand=True, pady=10)
        
        # Wordlist Generation Tab
        wordlist_frame = ttk.Frame(notebook)
        notebook.add(wordlist_frame, text="Wordlist Generator")
        
        # User inputs
        input_frame = ttk.LabelFrame(wordlist_frame, text="Personal Information", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Create input fields
        self.inputs = {}
        fields = [
            ("Full Name", "full_name"),
            ("Nickname", "nickname"),
            ("Pet Names", "pets"),
            ("Birth Year", "birth_year"),
            ("Company/School", "company"),
            ("Hobbies", "hobbies"),
            ("Other Keywords", "keywords")
        ]
        
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 3
            
            ttk.Label(input_frame, text=f"{label}:").grid(row=row, column=col, sticky='w', padx=5, pady=2)
            entry = ttk.Entry(input_frame, width=25)
            entry.grid(row=row, column=col+1, padx=5, pady=2)
            self.inputs[key] = entry
        
        # Generation options
        options_frame = ttk.LabelFrame(wordlist_frame, text="Generation Options", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.include_leetspeak = tk.BooleanVar(value=True)
        self.include_years = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Include Leetspeak", 
                       variable=self.include_leetspeak).pack(side='left', padx=10)
        ttk.Checkbutton(options_frame, text="Include Years", 
                       variable=self.include_years).pack(side='left', padx=10)
        ttk.Checkbutton(options_frame, text="Include Numbers", 
                       variable=self.include_numbers).pack(side='left', padx=10)
        
        # Generate button
        ttk.Button(wordlist_frame, text="Generate Wordlist", 
                  command=self.generate_wordlist).pack(pady=10)
        
        # Wordlist display
        self.wordlist_text = scrolledtext.ScrolledText(wordlist_frame, height=15, width=80)
        self.wordlist_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Export button
        ttk.Button(wordlist_frame, text="Export Wordlist", 
                  command=self.export_wordlist).pack(pady=5)
        
        self.status_label = ttk.Label(wordlist_frame, text="Ready")
        self.status_label.pack(pady=5)
    
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def analyze_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to analyze")
            return
        
        analysis = self.analyzer.analyze_password(password)
        
        # Display results
        self.analysis_text.delete(1.0, tk.END)
        
        result = f"""PASSWORD ANALYSIS RESULTS
{'='*50}

Password: {'*' * len(password)}
Length: {analysis['length']} characters
Entropy: {analysis['entropy']:.2f} bits
Character Sets: {', '.join(analysis['character_sets'])}

STRENGTH ASSESSMENT:
Score: {analysis['strength_score']}/100
Rating: {analysis['strength_label']}

"""
        
        if analysis['patterns']:
            result += "SECURITY ISSUES FOUND:\n"
            for issue in analysis['patterns']:
                result += f"• {issue}\n"
            result += "\n"
        
        if analysis['recommendations']:
            result += "RECOMMENDATIONS:\n"
            for rec in analysis['recommendations']:
                result += f"• {rec}\n"
        
        self.analysis_text.insert(tk.END, result)
    
    def generate_wordlist(self):
        # Get user inputs
        user_data = {}
        for key, entry in self.inputs.items():
            value = entry.get().strip()
            if value:
                user_data[key] = value
        
        if not any(user_data.values()):
            messagebox.showwarning("Warning", "Please enter some personal information")
            return
        
        self.status_label.config(text="Generating wordlist...")
        self.root.update()
        
        # Generate wordlist in thread to prevent UI freezing
        def generate():
            try:
                wordlist = self.generator.generate_custom_wordlist(user_data)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_wordlist(wordlist))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generating wordlist: {e}"))
                self.root.after(0, lambda: self.status_label.config(text="Error"))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def display_wordlist(self, wordlist):
        self.wordlist_text.delete(1.0, tk.END)
        self.wordlist_text.insert(tk.END, f"Generated {len(wordlist)} passwords:\n\n")
        
        for word in wordlist[:1000]:  # Limit display to first 1000
            self.wordlist_text.insert(tk.END, f"{word}\n")
        
        if len(wordlist) > 1000:
            self.wordlist_text.insert(tk.END, f"\n... and {len(wordlist) - 1000} more passwords")
        
        self.current_wordlist = wordlist
        self.status_label.config(text=f"Generated {len(wordlist)} passwords")
    
    def export_wordlist(self):
        if not hasattr(self, 'current_wordlist') or not self.current_wordlist:
            messagebox.showwarning("Warning", "No wordlist to export. Generate one first.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Wordlist",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if self.generator.export_wordlist(self.current_wordlist, filename):
                messagebox.showinfo("Success", f"Wordlist exported to {filename}")
                self.status_label.config(text=f"Exported {len(self.current_wordlist)} passwords")
            else:
                messagebox.showerror("Error", "Failed to export wordlist")

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer & Wordlist Generator")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface")
    parser.add_argument("--analyze", type=str, help="Analyze password strength")
    parser.add_argument("--generate", action="store_true", help="Generate wordlist")
    parser.add_argument("--output", type=str, help="Output file for wordlist")
    
    args = parser.parse_args()
    
    if args.gui or not any([args.analyze, args.generate]):
        # Launch GUI
        root = tk.Tk()
        app = PasswordToolGUI(root)
        root.mainloop()
    
    elif args.analyze:
        # CLI password analysis
        analyzer = PasswordAnalyzer()
        analysis = analyzer.analyze_password(args.analyze)
        
        print("PASSWORD ANALYSIS RESULTS")
        print("=" * 50)
        print(f"Length: {analysis['length']} characters")
        print(f"Entropy: {analysis['entropy']:.2f} bits")
        print(f"Character Sets: {', '.join(analysis['character_sets'])}")
        print(f"Strength Score: {analysis['strength_score']}/100")
        print(f"Rating: {analysis['strength_label']}")
        
        if analysis['patterns']:
            print("\nSECURITY ISSUES:")
            for issue in analysis['patterns']:
                print(f"• {issue}")
        
        if analysis['recommendations']:
            print("\nRECOMMENDATIONS:")
            for rec in analysis['recommendations']:
                print(f"• {rec}")
    
    elif args.generate:
        # CLI wordlist generation
        generator = WordlistGenerator()
        
        print("Enter personal information for wordlist generation:")
        user_data = {}
        
        fields = ["name", "nickname", "pets", "birth_year", "company", "hobbies"]
        for field in fields:
            value = input(f"{field.replace('_', ' ').title()}: ").strip()
            if value:
                user_data[field] = value
        
        if user_data:
            wordlist = generator.generate_custom_wordlist(user_data)
            print(f"\nGenerated {len(wordlist)} passwords")
            
            if args.output:
                if generator.export_wordlist(wordlist, args.output):
                    print(f"Wordlist saved to {args.output}")
                else:
                    print("Error saving wordlist")
            else:
                # Display first 20 passwords
                print("\nSample passwords:")
                for word in wordlist[:20]:
                    print(word)
                if len(wordlist) > 20:
                    print(f"... and {len(wordlist) - 20} more")
        else:
            print("No information provided.")

if __name__ == "__main__":
    main()
