var pc = null;
var dataChannel = null;

function negotiate() {
    pc.addTransceiver('video', {direction: 'recvonly'});
    pc.addTransceiver('audio', {direction: 'recvonly'});
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        return pc.setRemoteDescription(answer);
    }).then(function() {
        console.log("create data channel")
        dataChannel = pc.createDataChannel("chat", {
            negotiated: false
        });
        dataChannel.addEventListener("open", function(event) {
            console.log("create data channel open")
            beginTransmission(dataChannel);
            start_motion_track()
        });
        dataChannel.addEventListener('close', function(event) {
            console.log("create data channel close")
            messageBox.disabled = false;
            sendButton.disabled = false;
        });
    }).catch(function(e) {
        alert(e);
    });
}
function start_motion_track()
{
    //if (window.DeviceOrientationEvent) {
        window.addEventListener("deviceorientation", function(event) {
            // alpha: rotation around z-axis
            var rotateDegrees = event.alpha;
            // gamma: left to right
            var leftToRight = event.gamma;
            // beta: front back motion
            var frontToBack = event.beta;

            handleOrientationEvent(frontToBack, leftToRight, rotateDegrees);
        }, true);
    //}

    var handleOrientationEvent = function(frontToBack, leftToRight, rotateDegrees) {
        console.log("frontToBack:"+frontToBack+" leftToRight:"+leftToRight+" rotateDegrees:"+rotateDegrees)
    };
}
function go_fullscreen()
{
    //document.body.requestFullscreen();
}
function start() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    if (document.getElementById('use-stun').checked) {
        config.iceServers = [{urls: []}]; //'stun:stun.l.google.com:19302'
    }
    go_fullscreen()
    pc = new RTCPeerConnection(config);

    // connect audio / video
    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video') {
            document.getElementById('video_right').srcObject = evt.streams[0];
            document.getElementById('video_left').srcObject = evt.streams[0];
        } else {
            document.getElementById('audio').srcObject = evt.streams[0];
        }
    });

    document.getElementById('start_button').style.display = 'none';
    document.getElementById('media').style.display = 'inline-block';
    negotiate();
}

function stop() {
    document.getElementById('stop').style.display = 'none';
    setTimeout(function() {
        pc.close();
    }, 500);
}

if (window.DeviceOrientationEvent) {
    window.addEventListener("deviceorientation", function(event) {
        // alpha: rotation around z-axis
        var rotateDegrees = event.alpha;
        // gamma: left to right
        var leftToRight = event.gamma;
        // beta: front back motion
        var frontToBack = event.beta;

        handleOrientationEvent(frontToBack, leftToRight, rotateDegrees);
    }, true);
}

var handleOrientationEvent = function(frontToBack, leftToRight, rotateDegrees) {

};
