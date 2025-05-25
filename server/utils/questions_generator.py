import random
import ipaddress


class QuestionGenerator:

    @staticmethod
    def generate_ipv4_address(adr_type: str | list | None = None) -> str:

        if adr_type is None:
            adr_type = random.choice(('A', 'B', 'C'))

        if type(adr_type) == list:
            adr_type = random.choice(adr_type)

        address = ""
        mask = 0

        match adr_type.upper():
            case 'A':
                address = f"{random.randint(1, 125)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 253)}"
                mask = random.randint(8, 30)
            case 'B':
                address = f"{random.randint(128, 191)}.{random.randint(0, 254)}.{random.randint(0, 255)}.{random.randint(0, 253)}"
                mask = random.randint(16, 30)
            case 'C':
                address = f"{random.randint(192, 223)}.{random.randint(0, 255)}.{random.randint(0, 254)}.{random.randint(0, 253)}"
                mask = random.randint(24, 30)
            case 'D':
                address = f"{random.randint(224, 239)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                mask = 32

        return address + '/' + str(mask)

    @staticmethod
    def generate_netaddr_task():
        addr = QuestionGenerator.generate_ipv4_address()
        return {
            "type": "network_address",
            "question": addr,
            "corr_answer": str(ipaddress.IPv4Network(addr, strict=False).network_address),
            "student_answer": None
        }

    @staticmethod
    def generate_broadcast_task():
        addr = QuestionGenerator.generate_ipv4_address()
        return {
            "type": "broadcast_address",
            "question": addr,
            "corr_answer": str(ipaddress.IPv4Network(addr, strict=False).broadcast_address),
            "student_answer": None
        }

    @staticmethod
    def generate_fl_addr_task():
        addr = QuestionGenerator.generate_ipv4_address()
        network = ipaddress.IPv4Network(addr, strict=False)

        return {
            "type": "fl_address",
            "question": str(addr),
            "corr_answer": {
                "first": str(network[0]),
                "last": str(network[-1])
            },
            "student_answer": None
        }

    @staticmethod
    def generate_same_network_task():

        network = ipaddress.IPv4Network(QuestionGenerator.generate_ipv4_address(['A', 'B', 'C']), strict=False)
        mask = network.netmask
        same = random.randint(0, 1)

        addr1 = network[random.randint(0, network.num_addresses - 1)]
        addr2 = network[random.randint(0, network.num_addresses - 1)] if same else \
        QuestionGenerator.generate_ipv4_address().split("/")[0]

        return {
            "type": "same_network",
            "question": [f"{addr1} {mask}", f"{addr2} {mask}"],
            "corr_answer": same,
            "student_answer": None
        }

    @staticmethod
    def generate_mask_count_task():
        power = random.randint(8, 16)
        network = ipaddress.IPv4Network(f"0.0.0.0/{power}", strict=False)

        return {
            "type": "mask_count",
            "question": str(2 ** power),
            "corr_answer": str(network.netmask),
            "student_answer": None
        }

    @staticmethod
    def generate_mask_range_task():
        network = ipaddress.IPv4Network(QuestionGenerator.generate_ipv4_address(['A', 'B', 'C']), strict=False)

        return {
            "type": "mask_range",
            "question": [str(network[0]), str(network[-1])],
            "corr_answer": str(network.netmask),
            "student_answer": None
        }

    @staticmethod
    def generate_host_addr_task():
        address = QuestionGenerator.generate_ipv4_address(['A', 'B', 'C'])
        network = ipaddress.IPv4Network(address, strict=False)
        address = ipaddress.IPv4Address(address.split("/")[0])

        return {
            "type": "host_addr",
            "question": str(address),
            "corr_answer": not any((address == network.network_address,
                                    address.is_loopback, address.is_multicast,
                                    address == network.broadcast_address, address.is_reserved)),
            "student_answer": None
        }

    @staticmethod
    def generate_questions(counts: dict):

        functions = {
            "network_address": QuestionGenerator.generate_netaddr_task,
            "broadcast_address": QuestionGenerator.generate_broadcast_task,
            "first_last_address": QuestionGenerator.generate_fl_addr_task,
            "same_network": QuestionGenerator.generate_same_network_task,
            "mask_count": QuestionGenerator.generate_mask_count_task,
            "mask_range": QuestionGenerator.generate_mask_range_task,
            "host_addr": QuestionGenerator.generate_host_addr_task

        }

        result = []

        for task_type, count in counts.items():
            result.extend([functions[task_type]() for _ in range(count)])

        return result
