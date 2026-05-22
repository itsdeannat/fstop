from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import Client, Project, Booking, Gallery
from .serializers import ClientSerializer, ProjectSerializer, BookingSerializer, GallerySerializer, BadRequestSerializer, NotFoundSerializer, UnauthorizedSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiRequest
from drf_spectacular.types import OpenApiTypes

# Create your views here.


class ClientViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    @extend_schema(
        operation_id="list_clients",
        description="Get a list of all clients",
        responses={
            200: ClientSerializer(many=True),
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
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
                name="Bad Request",
                description="The JSON request body could not be parsed",
                value={"detail": "Invalid JSON in request body."},
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
    def list(self, request, *args, **kwargs):
        """Get all clients"""
        return super().list(request, *args, **kwargs)
 
    @extend_schema(
        operation_id="create_client",
        description="Create a new client",
        request=ClientSerializer,
        responses={
            201: ClientSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
        },
        examples=[
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
        description="Retrieve a single client by ID",
        responses={
            200: ClientSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        description="Update an existing client",
        request=ClientSerializer,
        responses={
            200: ClientSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        operation_id="delete_client",
        description="Delete a client",
        responses={
            204: None,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
    serializer_class = ProjectSerializer
 
    def get_queryset(self):
        queryset = Project.objects.all()
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset
 
    @extend_schema(
        operation_id="list_projects",
        description="Retrieve a list of all projects. Optionally filter by client_id query parameter. Returns an empty list if no clients match the filter.",
        responses={
            200: ProjectSerializer(many=True),
            401: UnauthorizedSerializer,
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
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440001",
                        "project_name": "Family Portraits",
                        "project_type": "portrait",
                        "client": {
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
                        "created_at": "2026-05-21T10:20:00Z",
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
        description="Create a new project for a client",
        request=ProjectSerializer,
        responses={
            201: ProjectSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
        },
        examples=[
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
        description="Retrieve a single project by ID",
        responses={
            200: ProjectSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        description="Update an existing project",
        request=ProjectSerializer,
        responses={
            200: ProjectSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        operation_id="delete_project",
        description="Delete a project",
        responses={
            204: None,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
    serializer_class = BookingSerializer
 
    def get_queryset(self):
        queryset = Booking.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
 
    @extend_schema(
        operation_id="list_bookings",
        description="Retrieve a list of all bookings. Optionally filter by project_id query parameter. Returns an empty list if no projects match the filter.",
        responses={
            200: BookingSerializer(many=True),
            401: UnauthorizedSerializer,
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
        description="Create a new booking for a project",
        request=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
        },
        examples=[
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
        description="Retrieve a single booking by ID",
        responses={
            200: BookingSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        description="Update an existing booking",
        request=BookingSerializer,
        responses={
            200: BookingSerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        operation_id="delete_booking",
        description="Delete a booking",
        responses={
            204: None,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
    serializer_class = GallerySerializer
 
    def get_queryset(self):
        queryset = Gallery.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
 
    @extend_schema(
        operation_id="list_galleries",
        description="Retrieve a list of all galleries. Optionally filter by project_id query parameter. Returns an empty list if no projects match the filter.",
        responses={
            200: GallerySerializer(many=True),
            401: UnauthorizedSerializer,
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
        description="Create a new gallery for a project",
        request=GallerySerializer,
        responses={
            201: GallerySerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
        },
        examples=[
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
        description="Retrieve a single gallery by ID",
        responses={
            200: GallerySerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        description="Update an existing gallery",
        request=GallerySerializer,
        responses={
            200: GallerySerializer,
            400: BadRequestSerializer,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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
        operation_id="delete_gallery",
        description="Delete a gallery",
        responses={
            204: None,
            401: UnauthorizedSerializer,
            404: NotFoundSerializer,
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