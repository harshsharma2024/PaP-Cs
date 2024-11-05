from sympy import symbols, Poly, simplify
import random
import time
import matplotlib.pyplot as plt

timegap = 2

x = symbols('x')

class User:
    def __init__(self, user_id, group_size,group_id, set_size=5):
        self.user_id = user_id
        self.gid = group_id 
        self.group_size = group_size
        self.self_mask = None
        self.inter_user_masks = []  # Initialize list to store masks generated for other users
        self.power = random.randint(1, set_size)
        self.set_size = set_size # maximum degree of the polynomial
        self.received_masks = [0] * (set_size + 1)
        self.fellow_users = [] # List of other users in the group

    def generate_nonzero_coefficient(self):
        coefficient = 0
        while coefficient == 0:
            coefficient = random.randint(-2, 2)
        return coefficient


    def update_group(self, users):
        self.fellow_users = [user for user in users if user.user_id != self.user_id]
        self.total_mask = self.generate_self_mask()

    def generate_self_mask(self):
        coefficient = self.generate_nonzero_coefficient()
        self.power = random.randint(1, self.set_size)
        self.self_mask = coefficient
        return self.self_mask

    def generate_inter_user_mask(self):
        
        for i in range(self.group_size - 3):
            coefficient = self.generate_nonzero_coefficient()
            
            self.inter_user_masks.append(coefficient)
            self.total_mask += coefficient
        if self.total_mask == 0:
            temp = self.generate_nonzero_coefficient()
            self.inter_user_masks.append(temp)
            self.total_mask += temp
            self.inter_user_masks.append(-temp)
            self.total_mask -= temp
        else:
            temp = self.generate_nonzero_coefficient()
            self.total_mask += temp
            while self.total_mask == 0:
                self.total_mask -= temp
                temp = self.generate_nonzero_coefficient()
                self.total_mask += temp
            self.inter_user_masks.append(temp)
            self.inter_user_masks.append(-self.total_mask)
            self.total_mask -= self.total_mask


        assert self.total_mask == 0 # Ensure that the sum of all coefficients (masked) is zero

    def receive_masks(self, sent_mask):
        # Generate inter-user masks for all other users and share them
        self.received_masks[sent_mask[0]] += sent_mask[1]
        
    def share_masks(self):
        cnt = 0
        for entry in self.fellow_users:
            mask = (self.power, self.inter_user_masks[cnt])
            entry.receive_masks(mask)
            cnt += 1

    def calculate_masked_value(self):
        self.received_masks[self.power] += self.self_mask
        self.received_masks[self.gid] += 1

        # print("User", self.user_id, "Received the following masks:")
        # print(self.received_masks)
        return self.receive_masks

def aggregate_data(users, set_size = 5):
    # Aggregator function to sum all masked values
    
    result = [0] * (set_size + 1)

    for user in users:
        for i in range(set_size + 1):
            result[i] += user.received_masks[i]
    
    res = Poly(0, x)
    # polynomial from the aggregated data
    cnt = 0
    for i in range(set_size + 1):
        res += result[i] * x**cnt
        cnt += 1


    time.sleep(timegap * 1e-3)
    return res



def main(grp_size):

    start_time = time.time()

    # Initialize users
    users = []
    set_size = (max(int(grp_size * 0.05), 5))
    for i in range(grp_size):
        gid = random.randint(1,set_size)
        users.append(User(i+1, grp_size, gid, set_size))

    print(len(users))

    # Update group information for each user (Assume that the group is static and known to all users)
    for user in users:
        user.update_group(users)

    # Step 1: User Setup and Mask Generation
    for user in users:
        user.generate_inter_user_mask()


    # Step 2: Masking and Data Sharing
    for user in users:
        time.sleep(timegap * 1e-3)
        user.share_masks() # Consider the time taken to share masks (latency)


    for user in users:
        user.calculate_masked_value()

    # Step 3: Data Aggregation at the Aggregator
    result = aggregate_data(users,set_size)
    print(result)

    # Sum of coefficients of the aggregated polynomial
    sum_of_coefficients = sum(result.coeffs())
    if sum_of_coefficients != grp_size:
        print("Error in aggregation")
        raise ValueError("Aggregation failed: The sum of coefficients does not match the group size.")



    time_diff = time.time() - start_time

    return time_diff*1e3


# plot the graph

def plot_graph(group_sizes, time_ms):
    plt.figure(figsize=(12, 8))

    plt.plot(group_sizes, time_ms, marker='o', color='darkblue', linestyle='-', linewidth=2, markersize=8, label='Time vs Group Size')

    plt.xlabel('Group Size (users involved in MPC) (k)', fontsize=16, fontweight='bold')
    plt.ylabel('Time Taken (ms)', fontsize=16, fontweight='bold')

    plt.title('Group Size vs Time Taken', fontsize=18, fontweight='bold')

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(loc='upper left', fontsize=14, frameon=True, shadow=True, fancybox=True)

    plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.8)

    plt.tight_layout()
    plt.show()