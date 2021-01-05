
class Claimant:
    def __init__(self, name, claims):
        self.name = name
        self.claims = round(claims*2)/2  # round the value to the nearest 0.5 to avoid problems with math
        self.gets = 0

    def loss(self):
        return self.claims - self.gets


# Obtain the data from user input
estate_size = float(input('\nEstate size: '))

unsorted_list_of_claimants = []
while True:
    print('\nNEW CLAIMANT')
    name = input('Name: ')
    claims = float(input('Claim: '))

    new_claimant = Claimant(name, claims)
    unsorted_list_of_claimants.append(new_claimant)

    if input('Add another claimant? y/n: ').lower() != 'y':
        break

# Order the creditors from lowest to highest claim
claimants = sorted(unsorted_list_of_claimants, key=lambda claimant: claimant.claims, reverse=False)

# Check for negative numbers and change them to 0
if estate_size < 0:
    estate_size = 0

for c in claimants:
    if c.claims < 0:
        c.claims = 0

# Check if the process can be simplified by just paying off full claims
sum_of_all_claims = 0
for c in claimants:
    sum_of_all_claims += c.claims

if estate_size >= sum_of_all_claims:
    for c in claimants:
        c.gets = c.claims

else:
    # Divide the estate equally among all parties until each creditor has reached one-half of the original claim,
    # starting from the lowest creditor.

    num_of_claimants = len(claimants)

    claimants_left = num_of_claimants
    while claimants_left > 0 and estate_size > 0:
        equal_division = estate_size / claimants_left

        for c in claimants:
            if c.gets < c.claims/2:
                if equal_division > c.claims/2 - c.gets:
                    amount = c.claims/2 - c.gets
                    c.gets += amount

                    estate_size -= amount
                else:
                    amount = equal_division
                    c.gets += amount

                    estate_size -= amount
            else:
                claimants_left -= 1

    # Now, work in reverse. Start giving the highest-claim money from the estate
    # until the loss, the difference between the claim and the award, equals the loss for the next highest creditor.

    while estate_size > 1:
        for c in range(len(claimants), 0, -1):
            c -= 1

            if c > 0:
                lower_claimants_loss = claimants[c - 1].loss()
                current_claimants_loss = claimants[c].loss()

                if c != len(claimants)-1:
                    higher_claimants_loss = claimants[c + 1].loss()
                else:
                    higher_claimants_loss = None

                # case of multiple claimants with identical losses
                if current_claimants_loss == lower_claimants_loss or current_claimants_loss == higher_claimants_loss:
                    tmp_list_of_claimants = []  # tmp list of claimants to be awarded equally
                    next_lowest_claimant = None

                    for cl in range(len(claimants)-1, -1, -1):  # range in reversed order

                        if claimants[cl].loss() == current_claimants_loss:
                            tmp_list_of_claimants.append(int(cl))
                        else:
                            next_lowest_claimant = int(cl)
                            break

                    if next_lowest_claimant is not None:
                        next_lowest_claimants_loss = claimants[next_lowest_claimant].loss()
                        current_lacks = current_claimants_loss - next_lowest_claimants_loss
                    else:
                        current_lacks = current_claimants_loss

                    if tmp_list_of_claimants:
                        if estate_size/len(tmp_list_of_claimants) >= current_lacks:
                            for cl in tmp_list_of_claimants:
                                claimants[cl].gets += current_lacks

                                estate_size -= current_lacks

                        elif estate_size/len(tmp_list_of_claimants) < current_lacks:
                            amount = estate_size/len(tmp_list_of_claimants)
                            for cl in tmp_list_of_claimants:
                                claimants[cl].gets += amount

                                estate_size -= amount

                # case of single claimant with particular loss
                elif current_claimants_loss > lower_claimants_loss:
                    current_lacks = current_claimants_loss - lower_claimants_loss

                    if estate_size >= current_lacks:
                        claimants[c].gets += current_lacks

                        estate_size -= current_lacks

                    elif estate_size < current_lacks:
                        claimants[c].gets += estate_size

                        estate_size -= estate_size

print()
for c in claimants:
    print(f'{c.name} gets {round(c.gets, 2)}')
