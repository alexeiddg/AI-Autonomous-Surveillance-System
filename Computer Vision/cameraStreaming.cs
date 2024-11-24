using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class CameraStreaming : MonoBehaviour
{
    public Camera cameraToStream; // Assign the camera in the Unity Inspector
    private string serverUrl = "http://127.0.0.1:8000/stream/camera1"; // Replace with your server's URL

    void Start()
    {
        // Ensure a camera is assigned
        if (cameraToStream == null)
        {
            Debug.LogError("No camera assigned. Please assign a camera in the Inspector.");
            return;
        }

        // Start sending frames to the server
        StartCoroutine(StreamToServer());
    }

    IEnumerator StreamToServer()
    {
        while (true)
        {
            // Capture the current frame from the camera
            RenderTexture currentRT = cameraToStream.targetTexture;
            RenderTexture.active = currentRT;

            Texture2D image = new Texture2D(currentRT.width, currentRT.height, TextureFormat.RGB24, false);
            image.ReadPixels(new Rect(0, 0, currentRT.width, currentRT.height), 0, 0);
            image.Apply();

            // Convert the captured frame to bytes
            byte[] imageBytes = image.EncodeToPNG();
            Destroy(image);

            Debug.Log($"Captured frame size: {imageBytes.Length} bytes");

            // Send the image to the server via POST request
            UnityWebRequest request = new UnityWebRequest(serverUrl, "POST");
            request.uploadHandler = new UploadHandlerRaw(imageBytes);
            request.SetRequestHeader("Content-Type", "application/octet-stream");
            request.downloadHandler = new DownloadHandlerBuffer();

            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Error sending frame: {request.error}");
            }
            else
            {
                Debug.Log($"Server response: {request.downloadHandler.text}");
            }

            // Frequency of sending frames
            yield return new WaitForSeconds(0.1f); // Adjust for performance (10 FPS here)
        }
    }
}
