#!/usr/bin/env python3
"""
Example script demonstrating Google Maps tool usage with the SearchAgent.

This script shows how to:
1. Search for places using Google Maps
2. Get detailed information about places
3. Create interactive map visualizations

Usage:
    python examples/maps_example.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import SearchAgent
from src.tools import google_maps_search, create_map_visualization


def example_1_direct_maps_search():
    """Example 1: Direct use of Google Maps search tool."""
    print("=" * 80)
    print("Example 1: Direct Google Maps Search")
    print("=" * 80)
    
    # Search for restaurants in Hong Kong
    print("\nSearching for 'Italian restaurants' in 'Tsim Sha Tsui, Hong Kong'...")
    result = google_maps_search(
        query="Italian restaurants",
        location="Tsim Sha Tsui, Hong Kong",
        num=5
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"\nFound {len(result['places'])} places:")
    for i, place in enumerate(result['places'], 1):
        print(f"\n{i}. {place['title']}")
        print(f"   Address: {place['address']}")
        print(f"   Rating: {place['rating']} ({place['reviews']} reviews)")
        print(f"   Category: {place['category']}")
        if place['phone']:
            print(f"   Phone: {place['phone']}")
        if place['website']:
            print(f"   Website: {place['website']}")
    
    # Create map visualization
    print("\n\nCreating map visualization...")
    map_result = create_map_visualization(
        places=result['places'],
        output_file="examples/italian_restaurants_map.html"
    )
    
    if "error" in map_result:
        print(f"Error creating map: {map_result['error']}")
    else:
        print(f"Map created successfully!")
        print(f"File: {map_result['file']}")
        print(f"Markers: {map_result['num_markers']}")
        print(f"Center: ({map_result['center']['lat']:.4f}, {map_result['center']['lng']:.4f})")
        print(f"\nOpen {map_result['file']} in your browser to view the map.")


def example_2_agent_with_maps():
    """Example 2: Using SearchAgent with Google Maps tools."""
    print("\n\n" + "=" * 80)
    print("Example 2: Agent with Google Maps Integration")
    print("=" * 80)
    
    # Initialize agent with maps enabled
    agent = SearchAgent(
        model="deepseek-chat",
        temperature=0.0,
        max_steps=5,
        use_tools=True,
        enable_maps=True
    )
    
    # Ask the agent to find and map coffee shops
    question = "Find the top 5 coffee shops in Central, Hong Kong and create a map showing their locations."
    
    print(f"\nQuestion: {question}")
    print("\nAgent is working...")
    
    result = agent.solve(question)
    
    print("\n--- Agent Response ---")
    print(result['final_answer'])
    
    print("\n--- Tool Calls ---")
    for i, tool_call in enumerate(result['tool_calls'], 1):
        print(f"\n{i}. Step {tool_call['step']}: {tool_call['tool']}")
        for key, value in tool_call.items():
            if key not in ['step', 'tool']:
                print(f"   {key}: {value}")


def example_3_tourist_attractions():
    """Example 3: Finding and mapping tourist attractions."""
    print("\n\n" + "=" * 80)
    print("Example 3: Tourist Attractions with Visualization")
    print("=" * 80)
    
    # Search for tourist attractions
    print("\nSearching for tourist attractions in Hong Kong...")
    result = google_maps_search(
        query="tourist attractions",
        location="Hong Kong",
        num=10
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"\nFound {len(result['places'])} attractions:")
    for i, place in enumerate(result['places'], 1):
        print(f"{i}. {place['title']} - Rating: {place['rating']}")
    
    # Create map
    print("\nCreating interactive map...")
    map_result = create_map_visualization(
        places=result['places'],
        output_file="examples/hong_kong_attractions_map.html"
    )
    
    if "error" not in map_result:
        print(f"\n✓ Map saved to: {map_result['file']}")
        print(f"  Open it in your browser to explore the attractions!")


def example_4_multi_category_search():
    """Example 4: Comparing multiple types of places."""
    print("\n\n" + "=" * 80)
    print("Example 4: Multi-Category Comparison")
    print("=" * 80)
    
    location = "Causeway Bay, Hong Kong"
    categories = ["cafes", "bookstores", "parks"]
    
    all_places = []
    
    for category in categories:
        print(f"\nSearching for {category} in {location}...")
        result = google_maps_search(
            query=category,
            location=location,
            num=3
        )
        
        if "error" not in result:
            print(f"Found {len(result['places'])} {category}")
            all_places.extend(result['places'])
    
    if all_places:
        print(f"\n\nCreating combined map with {len(all_places)} places...")
        map_result = create_map_visualization(
            places=all_places,
            output_file="examples/causeway_bay_combined_map.html"
        )
        
        if "error" not in map_result:
            print(f"\n✓ Combined map saved to: {map_result['file']}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Google Maps Tool Examples" + " " * 33 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\nThis script demonstrates various ways to use Google Maps tools.")
    print("Make sure your Serper-API key is set in .env file.\n")
    
    try:
        # Run examples
        example_1_direct_maps_search()
        
        # Uncomment to run other examples
        # example_2_agent_with_maps()
        # example_3_tourist_attractions()
        # example_4_multi_category_search()
        
        print("\n\n" + "=" * 80)
        print("Examples completed!")
        print("=" * 80)
        print("\nNote: To run other examples, uncomment them in the main block.")
        
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

