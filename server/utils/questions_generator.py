import random
import ipaddress
from typing import Dict, List


class QuestionGenerator:

    @staticmethod
    def generate_ipv4_address(addr_type: str | None = None) -> ipaddress.IPv4Network:

        if addr_type is None:
            addr_type = random.choice(('A', 'B', 'C'))

        address = ""
        mask = 0

        match addr_type.upper():
            case 'A':
                address = f"{random.randint(1, 125)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 253)}"
                mask = random.randint(8, 30)
            case 'B':
                address = f"{random.randint(128, 191)}.{random.randint(0, 254)}.{random.randint(0, 255)}.{random.randint(0, 253)}"
                mask = random.randint(16, 30)
            case 'C':
                address = f"{random.randint(192, 223)}.{random.randint(0, 255)}.{random.randint(0, 254)}.{random.randint(0, 253)}"
                mask = random.randint(24, 30)

        return ipaddress.IPv4Network(address + '/' + str(mask), strict=False)

    @staticmethod
    def generate_netaddr_task() -> Dict:
        addr = QuestionGenerator.generate_ipv4_address()
        return {
            "type": "network_address",
            "question": str(addr),
            "correct_answer": str(addr.network_address)
        }

    @staticmethod
    def generate_broadcast_task() -> Dict:
        addr = QuestionGenerator.generate_ipv4_address()
        return {
            "type": "broadcast_address",
            "question": str(addr),
            "correct_answer": str(addr.broadcast_address)
        }

    @staticmethod
    def generate_fl_addr_task() -> Dict:
        addr = QuestionGenerator.generate_ipv4_address()
        return {
            "question": str(addr),
            "first": ...,
            "last": ...
        }

    # FIXME: Сделать так, чтобы адреса были из одной сети с вероятностью 50%
    @staticmethod
    def generate_same_network_task() -> Dict:
        addr1 = QuestionGenerator.generate_ipv4_address()
        addr2 = QuestionGenerator.generate_ipv4_address()

        return {
            "type": "first_last_address",
            "question": [str(addr1), str(addr2)],
            "corr_answer": True if addr1 == addr2 else False
        }

    @staticmethod
    def generate_questions(counts: Dict) -> List:

        functions = {
            "network_address": QuestionGenerator.generate_netaddr_task,
            "broadcast_address": QuestionGenerator.generate_broadcast_task,
            "first_last_address": QuestionGenerator.generate_fl_addr_task
        }

        result = []

        for q_type, count in counts.items():
            result.extend([functions[q_type]() for _ in range(count)])

        return result

