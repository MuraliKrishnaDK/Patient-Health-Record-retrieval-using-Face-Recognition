import tensorflow as tf
import sys
import os
import rimage
def main():
    cnt=0
    # Disable tensorflow compilation warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    import tensorflow as tf

    # image_path = "akki.jpg"
    # image_data = tf.io.gfile.GFile(image_path, 'rb').read()


    rimage.main()
    image_data = tf.io.gfile.GFile("in.jpg", 'rb').read()
    


    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.io.gfile.GFile("logs/output_labels.txt")]

    # Unpersists graph from file
    with tf.io.gfile.GFile("logs/output_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            #print(human_string)
            score = predictions[0][node_id]
            if cnt==0:
                res=label_lines[node_id]
                res2=score*100
                res2=str(res2)
                res2=res2[0:4]
                cnt=cnt+1
            if float(res2)<60:
                print("unknown face")
                res="unknown"
            else:
                print ("result is ",res,res2)
                
            print('%s (score = %.5f)' % (human_string, score))
        return res
#main("dataset/srk/17.jpg")
