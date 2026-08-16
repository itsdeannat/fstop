from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Client, Project, Booking, Gallery
from .serializers import (
    ClientSerializer,
    ClientCreateSerializer,
    ProjectSerializer,
    ProjectCreateSerializer,
    BookingSerializer,
    BookingCreateSerializer,
    GallerySerializer,
    GalleryCreateSerializer,
    BadRequestSerializer,
    UnauthorizedSerializer,
    NotFoundSerializer,
    UserSignupSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwner, IsClientOwnerViaProject

# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    
    serializer_class = ClientSerializer
    
    def get_queryset(self):
        """Only return clients owned by the requesting user"""
        return Client.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Auto-assign the owner when creating a new client"""
        serializer.save(user=self.request.user)

    @extend_schema(
        operation_id="list_clients",
        summary="List all clients",
        description="Retrieve a list of all clients in the system.",
        responses={
            200: OpenApiResponse(response=ClientSerializer(many=True), description="List of clients retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="List of clients",
                value=[
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "first_name": "John",
                        "last_name": "Doe",
                        "city": "Oxford",
                        "state": "OH",
                        "zip_code": "45056",
                        "email": "john.doe@example.com",
                        "phone_number": "+12161231234",
                        "created_at": "2026-05-21T10:00:00Z",
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "city": "Columbus",
                        "state": "OH",
                        "zip_code": "43215",
                        "email": "jane.smith@example.com",
                        "phone_number": "+12161235678",
                        "created_at": "2026-05-21T10:05:00Z",
                    },
                ],
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Get all clients"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_client",
        summary="Create a client",
        description="Create a new client.",
        request=ClientCreateSerializer,
        responses={
            201: OpenApiResponse(response=ClientSerializer, description="Client created successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Request",
                description="Example client creation request",
                value={
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "city": "Cincinnati",
                    "state": "OH",
                    "zip_code": "45202",
                    "email": "alice.johnson@example.com",
                    "phone_number": "+12161239999",
                },
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Successful Response",
                description="Client created successfully",
                value={
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "city": "Cincinnati",
                    "state": "OH",
                    "zip_code": "45202",
                    "email": "alice.johnson@example.com",
                    "phone_number": "+12161239999",
                    "created_at": "2026-05-21T10:10:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid client data provided",
                value={"email": ["Enter a valid email address."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new client"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="retrieve_client",
        summary="Retrieve a client",
        description="Get a specific client by ID.",
        responses={
            200: OpenApiResponse(response=ClientSerializer, description="Client retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Client not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Single client details",
                value={
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "first_name": "John",
                    "last_name": "Doe",
                    "city": "Cleveland",
                    "state": "OH",
                    "zip_code": "44122",
                    "email": "john.doe@example.com",
                    "phone_number": "+12161231234",
                    "created_at": "2026-05-21T10:00:00Z",
                },
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Client does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def retrieve(self, request, pk=None):
        """Get a single client by ID"""
        return super().retrieve(request, pk=pk)

    @extend_schema(
        operation_id="update_client",
        summary="Update a client",
        description="Update an existing client.",
        request=ClientCreateSerializer,
        responses={
            200: OpenApiResponse(response=ClientSerializer, description="Client updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Client not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Client updated successfully",
                value={
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "first_name": "John",
                    "last_name": "Doe Updated",
                    "city": "Cleveland",
                    "state": "OH",
                    "zip_code": "44122",
                    "email": "john.updated@example.com",
                    "phone_number": "+12161231234",
                    "created_at": "2026-05-21T10:00:00Z",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid client data provided",
                value={"email": ["Enter a valid email address."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Client does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def update(self, request, pk=None):
        """Update an existing client"""
        return super().update(request, pk=pk)

    @extend_schema(
        operation_id="partially_update_client",
        summary="Partially update a client",
        description="Partially update an existing client.",
        request=ClientCreateSerializer,
        responses={
            200: OpenApiResponse(response=ClientSerializer, description="Client partially updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Client not found"),
        },
    )
    def partial_update(self, request, pk=None):
        """Partially update an existing client"""
        return super().partial_update(request, pk=pk)

    @extend_schema(
        operation_id="delete_client",
        summary="Delete a client",
        description="Delete a client by ID.",
        responses={
            204: OpenApiResponse(description="Client deleted successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Client not found"),
        },
        examples=[
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Client does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def destroy(self, request, pk=None):
        """Delete a client"""
        return super().destroy(request, pk=pk)


class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientOwnerViaProject]
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Only return projects whose clients are owned by the requesting user"""
        queryset = Project.objects.filter(client__user=self.request.user)
        # Allow filtering by client_id (if they own that client)
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset
    
    def perform_create(self, serializer):
        """Validate that the user owns the client before creating a project"""
        client = serializer.validated_data['client']
        if client.user != self.request.user:
            raise PermissionDenied("You can only create projects for clients you own.")
        serializer.save()

    @extend_schema(
        operation_id="list_projects",
        summary="List all projects",
        description="Retrieve a list of all projects. Optionally filter by client_id.",
        responses={
            200: OpenApiResponse(response=ProjectSerializer(many=True), description="List of projects retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="List of projects",
                value=[
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                ],
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Get all projects, optionally filtered by client_id"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_project",
        summary="Create a project",
        description="Create a new project for a client.",
        request=ProjectCreateSerializer,
        responses={
            201: OpenApiResponse(response=ProjectSerializer, description="Project created successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Request",
                description="Example project creation request",
                value={
                    "project_name": "Birthday Party",
                    "project_type": "party",
                    "client_id": "550e8400-e29b-41d4-a716-446655440002",
                },
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Successful Response",
                description="Project created successfully",
                value={
                    "id": "660e8400-e29b-41d4-a716-446655440002",
                    "project_name": "Birthday Party",
                    "project_type": "party",
                    "client": {
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "first_name": "Alice",
                        "last_name": "Johnson",
                        "city": "Cincinnati",
                        "state": "OH",
                        "zip_code": "45202",
                        "email": "alice.johnson@example.com",
                        "phone_number": "+12161239999",
                        "created_at": "2026-05-21T10:10:00Z",
                    },
                    "created_at": "2026-05-21T10:25:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid project data provided",
                value={"project_type": ["\"invalid\" is not a valid choice."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new project"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="retrieve_project",
        summary="Retrieve a project",
        description="Get a specific project by ID.",
        responses={
            200: OpenApiResponse(response=ProjectSerializer, description="Project retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Project not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Single project details",
                value={
                    "id": "660e8400-e29b-41d4-a716-446655440000",
                    "project_name": "Wedding",
                    "project_type": "event",
                    "client": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "first_name": "John",
                        "last_name": "Doe",
                        "city": "Cleveland",
                        "state": "OH",
                        "zip_code": "44122",
                        "email": "john.doe@example.com",
                        "phone_number": "+12161231234",
                        "created_at": "2026-05-21T10:00:00Z",
                    },
                    "created_at": "2026-05-21T10:15:00Z",
                },
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Project does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def retrieve(self, request, pk=None):
        """Get a single project by ID"""
        return super().retrieve(request, pk=pk)

    @extend_schema(
        operation_id="update_project",
        summary="Update a project",
        description="Update an existing project.",
        request=ProjectCreateSerializer,
        responses={
            200: OpenApiResponse(response=ProjectSerializer, description="Project updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Project not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Project updated successfully",
                value={
                    "id": "660e8400-e29b-41d4-a716-446655440000",
                    "project_name": "Wedding - Updated",
                    "project_type": "event",
                    "client": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "first_name": "John",
                        "last_name": "Doe",
                        "city": "Cleveland",
                        "state": "OH",
                        "zip_code": "44122",
                        "email": "john.doe@example.com",
                        "phone_number": "+12161231234",
                        "created_at": "2026-05-21T10:00:00Z",
                    },
                    "created_at": "2026-05-21T10:15:00Z",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid project data provided",
                value={"project_type": ["\"invalid\" is not a valid choice."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Project does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def update(self, request, pk=None):
        """Update an existing project"""
        return super().update(request, pk=pk)

    @extend_schema(
        operation_id="partially_update_project",
        summary="Partially update a project",
        description="Partially update an existing project.",
        request=ProjectCreateSerializer,
        responses={
            200: OpenApiResponse(response=ProjectSerializer, description="Project partially updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Project not found"),
        },
    )
    def partial_update(self, request, pk=None):
        """Partially update an existing project"""
        return super().partial_update(request, pk=pk)

    @extend_schema(
        operation_id="delete_project",
        summary="Delete a project",
        description="Delete a project by ID.",
        responses={
            204: OpenApiResponse(description="Project deleted successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Project not found"),
        },
        examples=[
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Project does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def destroy(self, request, pk=None):
        """Delete a project"""
        return super().destroy(request, pk=pk)


class BookingViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientOwnerViaProject]
    
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Only return bookings for projects whose clients are owned by the requesting user"""
        queryset = Booking.objects.filter(project__client__user=self.request.user)
        # Allow filtering by project_id (if they own that project's client)
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    def perform_create(self, serializer):
        """Validate that the user owns the project before creating a booking"""
        project = serializer.validated_data['project']
        if project.client.user != self.request.user:
            raise PermissionDenied("You can only create bookings for projects you own.")
        serializer.save()

    @extend_schema(
        operation_id="list_bookings",
        summary="List all bookings",
        description="Retrieve a list of all bookings. Optionally, filter by project_id.",
        responses={
            200: OpenApiResponse(response=BookingSerializer(many=True), description="List of bookings retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="List of bookings",
                value=[
                    {
                        "id": "770e8400-e29b-41d4-a716-446655440000",
                        "project": {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "project_name": "Wedding",
                            "project_type": "event",
                            "client": {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "first_name": "John",
                                "last_name": "Doe",
                                "city": "Cleveland",
                                "state": "OH",
                                "zip_code": "44122",
                                "email": "john.doe@example.com",
                                "phone_number": "+12161231234",
                                "created_at": "2026-05-21T10:00:00Z",
                            },
                            "created_at": "2026-05-21T10:15:00Z",
                        },
                        "date": "2026-06-15",
                        "time": "14:00:00",
                        "duration": 480,
                        "location": "Downtown Venue",
                        "created_at": "2026-05-21T10:30:00Z",
                    },
                ],
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Get all bookings, optionally filtered by project_id"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_booking",
        summary="Create a booking",
        description="Create a new booking for a project.",
        request=BookingCreateSerializer,
        responses={
            201: OpenApiResponse(response=BookingSerializer, description="Booking created successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Request",
                description="Example booking creation request",
                value={
                    "project_id": "660e8400-e29b-41d4-a716-446655440000",
                    "date": "2026-06-15",
                    "time": "14:00:00",
                    "duration": 480,
                    "location": "Downtown Venue",
                },
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Successful Response",
                description="Booking created successfully",
                value={
                    "id": "770e8400-e29b-41d4-a716-446655440001",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "date": "2026-06-15",
                    "time": "14:00:00",
                    "duration": 480,
                    "location": "Downtown Venue",
                    "created_at": "2026-05-21T10:30:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid booking data provided",
                value={"duration": ["Ensure this value is greater than or equal to 0."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="retrieve_booking",
        summary="Retrieve a booking",
        description="Get a specific booking by ID.",
        responses={
            200: OpenApiResponse(response=BookingSerializer, description="Booking retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Booking not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Single booking details",
                value={
                    "id": "770e8400-e29b-41d4-a716-446655440000",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "date": "2026-06-15",
                    "time": "14:00:00",
                    "duration": 480,
                    "location": "Downtown Venue",
                    "created_at": "2026-05-21T10:30:00Z",
                },
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Booking does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def retrieve(self, request, pk=None):
        """Get a single booking by ID"""
        return super().retrieve(request, pk=pk)

    @extend_schema(
        operation_id="update_booking",
        summary="Update a booking",
        description="Update an existing booking.",
        request=BookingCreateSerializer,
        responses={
            200: OpenApiResponse(response=BookingSerializer, description="Booking updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Booking not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Booking updated successfully",
                value={
                    "id": "770e8400-e29b-41d4-a716-446655440000",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "date": "2026-06-16",
                    "time": "15:00:00",
                    "duration": 480,
                    "location": "Downtown Venue - Updated",
                    "created_at": "2026-05-21T10:30:00Z",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid booking data provided",
                value={"duration": ["Ensure this value is greater than or equal to 0."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Booking does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def update(self, request, pk=None):
        """Update an existing booking"""
        return super().update(request, pk=pk)

    @extend_schema(
        operation_id="partially_update_booking",
        summary="Partially update a booking",
        description="Partially update an existing booking.",
        request=BookingCreateSerializer,
        responses={
            200: OpenApiResponse(response=BookingSerializer, description="Booking partially updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Booking not found"),
        },
    )
    def partial_update(self, request, pk=None):
        """Partially update an existing booking"""
        return super().partial_update(request, pk=pk)

    @extend_schema(
        operation_id="delete_booking",
        summary="Delete a booking",
        description="Delete a booking by ID.",
        responses={
            204: OpenApiResponse(description="Booking deleted successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Booking not found"),
        },
        examples=[
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Booking does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def destroy(self, request, pk=None):
        """Delete a booking"""
        return super().destroy(request, pk=pk)


class GalleryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsClientOwnerViaProject]
    
    serializer_class = GallerySerializer

    def get_queryset(self):
        """Only return galleries for projects whose clients are owned by the requesting user"""
        queryset = Gallery.objects.filter(project__client__user=self.request.user)
        # Allow filtering by project_id (if they own that project's client)
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    def perform_create(self, serializer):
        """Validate that the user owns the project before creating a gallery"""
        project = serializer.validated_data['project']
        if project.client.user != self.request.user:
            raise PermissionDenied("You can only create galleries for projects you own.")
        serializer.save()

    @extend_schema(
        operation_id="list_galleries",
        summary="List all galleries",
        description="Retrieve a list of all galleries. Optionally filter by project_id.",
        responses={
            200: OpenApiResponse(response=GallerySerializer(many=True), description="List of galleries retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="List of galleries",
                value=[
                    {
                        "id": "880e8400-e29b-41d4-a716-446655440000",
                        "project": {
                            "id": "660e8400-e29b-41d4-a716-446655440000",
                            "project_name": "Wedding",
                            "project_type": "event",
                            "client": {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "first_name": "John",
                                "last_name": "Doe",
                                "city": "Cleveland",
                                "state": "OH",
                                "zip_code": "44122",
                                "email": "john.doe@example.com",
                                "phone_number": "+12161231234",
                                "created_at": "2026-05-21T10:00:00Z",
                            },
                            "created_at": "2026-05-21T10:15:00Z",
                        },
                        "gallery_name": "Ceremony Photos",
                        "picture_count": 125,
                        "is_visible": True,
                        "url": "https://example.com/galleries/ceremony",
                        "created_at": "2026-05-21T10:35:00Z",
                    },
                ],
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        """Get all galleries, optionally filtered by project_id"""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_gallery",
        summary="Create a gallery",
        description="Create a new gallery for a project.",
        request=GalleryCreateSerializer,
        responses={
            201: OpenApiResponse(response=GallerySerializer, description="Gallery created successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
        },
        examples=[
            OpenApiExample(
                name="Request",
                description="Example gallery creation request",
                value={
                    "project_id": "660e8400-e29b-41d4-a716-446655440000",
                    "gallery_name": "Reception Photos",
                    "picture_count": 89,
                    "is_visible": True,
                    "url": "https://example.com/galleries/reception",
                },
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Successful Response",
                description="Gallery created successfully",
                value={
                    "id": "880e8400-e29b-41d4-a716-446655440001",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "gallery_name": "Reception Photos",
                    "picture_count": 89,
                    "is_visible": True,
                    "url": "https://example.com/galleries/reception",
                    "created_at": "2026-05-21T10:35:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid gallery data provided",
                value={"url": ["Enter a valid URL."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """Create a new gallery"""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        operation_id="retrieve_gallery",
        summary="Retrieve a gallery",
        description="Get a specific gallery by ID.",
        responses={
            200: OpenApiResponse(response=GallerySerializer, description="Gallery retrieved successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Gallery not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Single gallery details",
                value={
                    "id": "880e8400-e29b-41d4-a716-446655440000",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "gallery_name": "Ceremony Photos",
                    "picture_count": 125,
                    "is_visible": True,
                    "url": "https://example.com/galleries/ceremony",
                    "created_at": "2026-05-21T10:35:00Z",
                },
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Gallery does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def retrieve(self, request, pk=None):
        """Get a single gallery by ID"""
        return super().retrieve(request, pk=pk)

    @extend_schema(
        operation_id="update_gallery",
        summary="Update a gallery",
        description="Update an existing gallery.",
        request=GalleryCreateSerializer,
        responses={
            200: OpenApiResponse(response=GallerySerializer, description="Gallery updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Gallery not found"),
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                description="Gallery updated successfully",
                value={
                    "id": "880e8400-e29b-41d4-a716-446655440000",
                    "project": {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "project_name": "Wedding",
                        "project_type": "event",
                        "client": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "first_name": "John",
                            "last_name": "Doe",
                            "city": "Cleveland",
                            "state": "OH",
                            "zip_code": "44122",
                            "email": "john.doe@example.com",
                            "phone_number": "+12161231234",
                            "created_at": "2026-05-21T10:00:00Z",
                        },
                        "created_at": "2026-05-21T10:15:00Z",
                    },
                    "gallery_name": "Ceremony Photos - Updated",
                    "picture_count": 125,
                    "is_visible": False,
                    "url": "https://example.com/galleries/ceremony",
                    "created_at": "2026-05-21T10:35:00Z",
                },
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                name="Bad Request",
                description="Invalid gallery data provided",
                value={"url": ["Enter a valid URL."]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Gallery does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def update(self, request, pk=None):
        """Update an existing gallery"""
        return super().update(request, pk=pk)

    @extend_schema(
        operation_id="partially_update_gallery",
        summary="Partially update a gallery",
        description="Partially update an existing gallery.",
        request=GalleryCreateSerializer,
        responses={
            200: OpenApiResponse(response=GallerySerializer, description="Gallery partially updated successfully"),
            400: OpenApiResponse(response=BadRequestSerializer, description="Invalid request data"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Gallery not found"),
        },
    )
    def partial_update(self, request, pk=None):
        """Partially update an existing gallery"""
        return super().partial_update(request, pk=pk)

    @extend_schema(
        operation_id="delete_gallery",
        summary="Delete a gallery",
        description="Delete a gallery by ID.",
        responses={
            204: OpenApiResponse(description="Gallery deleted successfully"),
            401: OpenApiResponse(response=UnauthorizedSerializer, description="Authentication required"),
            404: OpenApiResponse(response=NotFoundSerializer, description="Gallery not found"),
        },
        examples=[
            OpenApiExample(
                name="Unauthorized",
                description="Missing authentication credentials",
                value={"detail": "Authentication credentials were not provided."},
                response_only=True,
                status_codes=["401"],
            ),
            OpenApiExample(
                name="Not Found",
                description="Gallery does not exist",
                value={"detail": "Not found."},
                response_only=True,
                status_codes=["404"],
            ),
        ],
    )
    def destroy(self, request, pk=None):
        """Delete a gallery"""
        return super().destroy(request, pk=pk)
    
@extend_schema_view(
    post=extend_schema(
        operation_id="obtain_token",
        summary="Obtain JWT token",
        description="Authenticate and obtain access and refresh tokens.",
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse({"type": "object", "properties": {
                "access": {"type": "string"},
                "refresh": {"type": "string"}
            }}, description="Successfully obtained JWT token"),
            400: OpenApiResponse(response=UnauthorizedSerializer, description="Invalid username or password")
        },
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

@extend_schema_view(
    post=extend_schema(
        operation_id="refresh_token",
        summary="Refresh JWT token",
        description="Refresh an expired access token using a refresh token.",
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse({"type": "object", "properties": {
                "access": {"type": "string"}
            }}, description="Successfully refreshed token"),
            400: OpenApiResponse(response=UnauthorizedSerializer, description="Invalid refresh token")
        },
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(exclude=True)
    def post(self, request):
        """
        Handles POST requests to create a new user in the database
        """
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)