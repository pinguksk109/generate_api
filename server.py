import grpc
from concurrent import futures
import proto.trivia_pb2
import proto.trivia_pb2_grpc
from application.usecase.trivia_quiz_usecase import TriviaQuizUsecase, TriviaQuizInput, TriviaQuizOutput
from application.config import AppConfig

class TriviaServiceServicer(trivia_pb2_grpc.TriviaServiceServicer):
    async def GenerateTrivia(self, request, context):
        config = AppConfig()
        input_data = TriviaQuizInput(config=config, category=request.category)

        usecase = TriviaQuizUsecase()
        usecase.input_data = input_data

        output_data = await usecase.handle()

        return trivia_pb2.TriviaResponse(
            quiz=output_data.item.quiz,
            choices=output_data.item.choices,
            answer=output_data.item.answer,
            explanation=output_data.item.explanation
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trivia_pb2_grpc.add_TriviaServiceServicer_to_server(TriviaServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()