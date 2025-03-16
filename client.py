import grpc
import trivia_pb2
import trivia_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = trivia_pb2_grpc.TriviaServiceStub(channel)
    
    request = trivia_pb2.TriviaRequest(category="うんこ")
    response = stub.GenerateTrivia(request)

    print(f"Quiz: {response.quiz}")
    print(f"Choices: {', '.join(response.choices)}")
    print(f"Answer: {response.answer}")
    print(f"Explanation: {response.explanation}")

if __name__ == "__main__":
    run()