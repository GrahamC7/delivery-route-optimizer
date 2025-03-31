# 🚚 Delivery Route Optimizer (WGUPS Simulation)

This Python application simulates an efficient package delivery system for the **Western Governors University Parcel Service (WGUPS)**. It uses the **Nearest Neighbor algorithm** for route optimization and a **custom-built hash table** for fast package lookup.

---

## 📦 Project Overview

The system was built to solve a logistics challenge:

- 40 packages  
- 3 trucks  
- Only 2 drivers (Truck 3 must wait for Truck 1 or 2 to return)  
- Deadline and constraint-based delivery  
- Goal: Complete all deliveries in under **140 total miles**

The simulation delivers packages efficiently, tracks real-time status, and provides tools for querying delivery data.

---

## 🧠 Key Features

- 🔄 **Greedy Nearest Neighbor** algorithm for route optimization  
- ⚡ **Custom hash table** with O(1) lookup for package management  
- ⏰ **Dynamic delivery tracking** by time, truck, or package ID  
- 🕹️ **Interactive command-line interface (CLI)**  
- 🧪 Fully modular codebase (easy to maintain or extend)

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+
- **Algorithm:** Nearest Neighbor (Greedy)
- **Data Structures:** Hash Table, List
- **Paradigm:** Object-Oriented Design (OOP)
- **Structure:** Modular architecture with clear separation of concerns

---

## 📂 Project Structure

delivery-route-optimizer/
├── data/
│   ├── address.csv
│   ├── distance.csv
│   └── packages.csv
├── src/
│   ├── main.py                  # Entry point
│   ├── interface.py             # Command-line interface
│   ├── models/
│   │   ├── hash_table.py
│   │   ├── package.py
│   │   └── truck.py
│   └── logic/
│       ├── data_loader.py
│       ├── routing.py
│       └── helpers.py
└── README.md

---

## 🚀 How to Run

**Requires:** Python 3.10+

Step 1: Navigate to the project root  
Step 2: Run the application

```bash
python src/main.py
```

Then follow the CLI prompts to interact with the system.

---

## 🧪 CLI Menu Options

1. Total mileage for all trucks  
2. Check status of a single package at a specific time  
3. View all packages at a specific time  
4. View packages on a truck at a specific time  
5. List assigned packages per truck  
6. Exit the application

---

## 📈 Example Output

📦 Package Status  
------------------------------  
Package ID   : 12  
Status       : Delivered  
Location     : 233 Canyon Rd  
Delivery Time: 09:42  
Deadline     : 10:30  

---

## 👨‍💻 Author

**Graham Cockerham**  
B.S. in Computer Science  
Software Engineer with interests in embedded systems, AI, and aerospace applications
https://github.com/GrahamC7

---

## 📄 License

This project is open source under the MIT License.  
https://opensource.org/licenses/MIT