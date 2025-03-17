import asyncio
import grpc.aio
from concurrent import futures
import trivia_pb2
import trivia_pb2_grpc
from application.usecase.trivia_quiz_usecase import TriviaQuizUsecase, TriviaQuizInput, TriviaQuizOutput
from application.config import state

class TriviaServiceServicer(trivia_pb2_grpc.TriviaServiceServicer):
    async def GenerateTrivia(self, request, context):
        config = state()
        input_data = TriviaQuizInput(config=config, category=request.category)

        usecase = TriviaQuizUsecase(input_data)

        output_data = await usecase.handle()

        return trivia_pb2.TriviaResponse(
            quiz=output_data.item.quiz,
            choices=output_data.item.choices,
            answer=output_data.item.answer,
            explanation=output_data.item.explanation
        )

async def serve():
    server = grpc.aio.server()
    trivia_pb2_grpc.add_TriviaServiceServicer_to_server(TriviaServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC async server is running on port 50051...")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())