from openai import OpenAI, APIError, RateLimitError, APIConnectionError
import os
import time
import logging
from functools import lru_cache
from typing import List, Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def call_llm(prompt: str = None, 
             messages: List[Dict[str, str]] = None, 
             model: str = None, 
             temperature: float = 0.7,
             max_retries: int = 3,
             use_cache: bool = True) -> str:
    """
    Enhanced LLM caller with error handling, caching, and retry logic.
    
    Args:
        prompt (str): Simple prompt string (alternative to messages)
        messages (List[Dict]): List of message dictionaries with role and content
        model (str): Model to use (defaults to environment variable)
        temperature (float): Temperature for generation
        max_retries (int): Maximum number of retry attempts
        use_cache (bool): Whether to use caching
        
    Returns:
        str: LLM response content
        
    Raises:
        Exception: If all retry attempts fail
    """
    # Set default model
    if model is None:
        model = os.environ.get("OPENROUTER_MODEL", "openrouter/anthropic/claude-3.5-sonnet")
    
    # Create messages if prompt is provided
    if prompt is not None:
        messages = [{"role": "user", "content": prompt}]
    elif messages is None:
        raise ValueError("Either prompt or messages must be provided")
    
    # Cache key for caching
    cache_key = f"{model}_{temperature}_{str(messages)}"
    
    # Check cache if enabled
    if use_cache and hasattr(call_llm, '_cache') and cache_key in call_llm._cache:
        logger.info("Cache hit for LLM call")
        return call_llm._cache[cache_key]
    
    # Initialize cache if not exists
    if not hasattr(call_llm, '_cache'):
        call_llm._cache = {}
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1" if "openrouter" in model else None,
        api_key=os.environ.get("OPENROUTER_API_KEY", os.environ.get("OPENAI_API_KEY", "your-api-key"))
    )
    
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            logger.info(f"LLM call attempt {attempt + 1}/{max_retries}")
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            result = response.choices[0].message.content
            
            # Cache the result if caching is enabled
            if use_cache:
                call_llm._cache[cache_key] = result
            
            logger.info("LLM call successful")
            return result
            
        except RateLimitError as e:
            last_exception = e
            wait_time = (2 ** attempt) + 1  # Exponential backoff
            logger.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}")
            time.sleep(wait_time)
            
        except APIConnectionError as e:
            last_exception = e
            wait_time = 2 ** attempt
            logger.warning(f"Connection error. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}")
            time.sleep(wait_time)
            
        except APIError as e:
            last_exception = e
            logger.error(f"API error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:  # Last attempt
                break
            time.sleep(2 ** attempt)
            
        except Exception as e:
            last_exception = e
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:  # Last attempt
                break
            time.sleep(2 ** attempt)
    
    # If we get here, all retries failed
    logger.error(f"All {max_retries} attempts failed. Last error: {last_exception}")
    raise Exception(f"LLM call failed after {max_retries} attempts: {last_exception}")

def clear_llm_cache():
    """Clear the LLM call cache."""
    if hasattr(call_llm, '_cache'):
        call_llm._cache.clear()
        logger.info("LLM cache cleared")

# Legacy function for backward compatibility
def call_llm_legacy(prompt):    
    """Legacy function for backward compatibility."""
    return call_llm(prompt=prompt)

if __name__ == "__main__":
    # Test the enhanced LLM caller
    print("Testing enhanced LLM caller...")
    
    try:
        # Test 1: Simple prompt
        prompt = "What is the meaning of life in one sentence?"
        print(f"Test 1 - Simple prompt: {prompt}")
        response1 = call_llm(prompt=prompt, use_cache=False)
        print(f"Response: {response1}")
        
        # Test 2: Messages format
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are the benefits of AI in marketing?"}
        ]
        print(f"\nTest 2 - Messages format")
        response2 = call_llm(messages=messages, use_cache=False)
        print(f"Response: {response2}")
        
        # Test 3: Cache functionality
        print(f"\nTest 3 - Cache test (should be fast)")
        start_time = time.time()
        response3 = call_llm(prompt=prompt, use_cache=True)  # This should use cache
        end_time = time.time()
        print(f"Response: {response3}")
        print(f"Cache test time: {end_time - start_time:.2f} seconds")
        
        # Test 4: Cache clear
        print(f"\nTest 4 - Clearing cache")
        clear_llm_cache()
        print("Cache cleared successfully")
        
    except Exception as e:
        print(f"Error during testing: {e}")
